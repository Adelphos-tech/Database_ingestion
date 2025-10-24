import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from pinecone import Pinecone, ServerlessSpec
import google.generativeai as genai
import hashlib
from datetime import datetime
import PyPDF2
import docx
import pandas as pd
from io import BytesIO
import traceback
from dotenv import load_dotenv
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import Document as LlamaDocument

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "DELETE", "OPTIONS"], "allow_headers": "*"}})

# Configuration - Set these in environment variables
PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Initialize clients
pc = Pinecone(api_key=PINECONE_API_KEY)

# Initialize Google Gemini for embeddings
print("Configuring Google Gemini embeddings...")
genai.configure(api_key=GEMINI_API_KEY)
print("✅ Google Gemini embeddings configured!")
print("✅ Using text-embedding-004 model (768 dimensions)")
print("✅ Matches n8n workflow embedding model")

# Index configuration
DEFAULT_INDEX_NAME = "document-knowledge-base"
EMBEDDING_DIMENSION = 768  # Google Gemini text-embedding-004 produces 768-dimensional embeddings

# Chunking configuration (using LlamaIndex's SentenceSplitter - Recursive Character Text Splitter)
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 300  # Increased overlap for better context retrieval


def get_or_create_index(index_name=None):
    """Get existing index or create new one"""
    try:
        if index_name is None:
            index_name = DEFAULT_INDEX_NAME
            
        existing_indexes = [index.name for index in pc.list_indexes()]
        
        if index_name not in existing_indexes:
            pc.create_index(
                name=index_name,
                dimension=EMBEDDING_DIMENSION,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region=PINECONE_ENVIRONMENT
                )
            )
        
        return pc.Index(index_name)
    except Exception as e:
        print(f"Error creating/getting index: {e}")
        raise


def extract_text_from_pdf(file_bytes):
    """Extract text from PDF file"""
    pdf_file = BytesIO(file_bytes)
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n\n"
    return text


def extract_text_from_docx(file_bytes):
    """Extract text from DOCX file"""
    doc_file = BytesIO(file_bytes)
    doc = docx.Document(doc_file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text


def extract_text_from_excel(file_bytes, filename):
    """Extract text from Excel file"""
    excel_file = BytesIO(file_bytes)
    
    if filename.endswith('.csv'):
        df = pd.read_csv(excel_file)
        return df.to_string()
    else:
        xls = pd.ExcelFile(excel_file)
        text = ""
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name)
            text += f"\n\n=== Sheet: {sheet_name} ===\n"
            text += df.to_string()
        return text


def extract_text(file_bytes, filename):
    """Route to appropriate text extraction based on file type (Default Data Loader functionality)"""
    extension = filename.lower().split('.')[-1]
    
    if extension == 'pdf':
        return extract_text_from_pdf(file_bytes)
    elif extension in ['docx', 'doc']:
        return extract_text_from_docx(file_bytes)
    elif extension in ['xlsx', 'xls', 'csv']:
        return extract_text_from_excel(file_bytes, filename)
    elif extension == 'txt':
        return file_bytes.decode('utf-8')
    else:
        raise ValueError(f"Unsupported file type: {extension}")


def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=CHUNK_OVERLAP):
    """Split text into overlapping chunks using LlamaIndex's Recursive Character Text Splitter"""
    # Create LlamaIndex Document
    document = LlamaDocument(text=text)
    
    # Initialize SentenceSplitter (LlamaIndex's recursive character text splitter)
    text_splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separator=" ",  # Default separator
    )
    
    # Split the document into nodes
    nodes = text_splitter.get_nodes_from_documents([document])
    
    # Convert nodes to our chunk format
    chunks = []
    for idx, node in enumerate(nodes):
        chunks.append({
            'text': node.text,
            'start_position': node.start_char_idx if hasattr(node, 'start_char_idx') else 0,
            'end_position': node.end_char_idx if hasattr(node, 'end_char_idx') else len(node.text),
            'chunk_index': idx
        })
    
    return chunks


def generate_embeddings(texts):
    """Generate embeddings using Google Gemini API (matches n8n workflow)"""
    embeddings = []
    
    # Process in batches to handle rate limits
    batch_size = 100
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        try:
            # Use Gemini's embedding model (same as n8n)
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=batch,
                task_type="retrieval_document"
            )
            embeddings.extend(result['embedding'])
        except Exception as e:
            print(f"Error generating embeddings for batch {i}: {e}")
            # Fallback: process one by one if batch fails
            for text in batch:
                try:
                    result = genai.embed_content(
                        model="models/text-embedding-004",
                        content=text,
                        task_type="retrieval_document"
                    )
                    embeddings.append(result['embedding'])
                except Exception as e2:
                    print(f"Error generating embedding: {e2}")
                    # Use zero vector as fallback
                    embeddings.append([0.0] * EMBEDDING_DIMENSION)
    
    return embeddings


def generate_document_id(filename, project):
    """Generate unique document ID"""
    timestamp = datetime.now().isoformat()
    unique_string = f"{filename}_{project}_{timestamp}"
    return hashlib.md5(unique_string.encode()).hexdigest()


@app.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({
        'message': 'Knowledge Base API is running!',
        'status': 'online',
        'endpoints': {
            'health': '/health',
            'upload': '/api/upload',
            'documents': '/api/documents',
            'indexes': '/api/indexes'
        }
    })


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'pinecone_configured': bool(PINECONE_API_KEY),
        'gemini_configured': bool(GEMINI_API_KEY),
        'embedding_model': 'Google Gemini text-embedding-004',
        'embedding_type': 'API - Matches n8n workflow',
        'embedding_dimension': EMBEDDING_DIMENSION,
        'quota_limits': 'Google Gemini API limits apply'
    })


@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Upload and index document to Pinecone"""
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        project = request.form.get('project', 'default')
        index_name = request.form.get('index_name', DEFAULT_INDEX_NAME)
        
        if file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # Read file
        file_bytes = file.read()
        filename = file.filename
        
        # Extract text
        text = extract_text(file_bytes, filename)
        
        if not text or len(text.strip()) == 0:
            return jsonify({'error': 'No text extracted from file'}), 400
        
        # Chunk text
        chunks = chunk_text(text)
        
        # Generate document ID
        doc_id = generate_document_id(filename, project)
        
        # Generate embeddings for all chunks
        chunk_texts = [chunk['text'] for chunk in chunks]
        embeddings = generate_embeddings(chunk_texts)
        
        # Prepare vectors for Pinecone
        index = get_or_create_index(index_name)
        vectors = []
        
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            vector_id = f"{doc_id}_chunk_{i}"
            metadata = {
                'document_id': doc_id,
                'filename': filename,
                'project': project,
                'chunk_index': i,
                'total_chunks': len(chunks),
                'text': chunk['text'],  # Store full chunk text for RAG retrieval
                'upload_date': datetime.now().isoformat(),
                'file_size': len(file_bytes),
                'chunk_start': chunk['start_position'],
                'chunk_end': chunk['end_position'],
                'source': filename  # Add source field for better context
            }
            
            vectors.append({
                'id': vector_id,
                'values': embedding,
                'metadata': metadata
            })
        
        # Upsert to Pinecone in batches
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            index.upsert(vectors=batch, namespace=project)
        
        return jsonify({
            'success': True,
            'document_id': doc_id,
            'filename': filename,
            'project': project,
            'chunks_created': len(chunks),
            'total_characters': len(text)
        })
        
    except Exception as e:
        print(f"Upload error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/search', methods=['POST'])
def search_documents():
    """Search documents using semantic search"""
    try:
        data = request.get_json()
        query = data.get('query', '')
        project = data.get('project', 'default')
        index_name = data.get('index_name', DEFAULT_INDEX_NAME)
        top_k = data.get('top_k', 10)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Generate query embedding
        query_embedding = generate_embeddings([query])[0]
        
        # Search in Pinecone
        index = get_or_create_index(index_name)
        results = index.query(
            vector=query_embedding,
            top_k=top_k,
            namespace=project,
            include_metadata=True
        )
        
        # Format results
        search_results = []
        for match in results.matches:
            search_results.append({
                'id': match.id,
                'score': float(match.score),
                'metadata': match.metadata
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'results': search_results,
            'total_results': len(search_results)
        })
        
    except Exception as e:
        print(f"Search error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents', methods=['GET'])
def list_documents():
    """List all documents in a project"""
    try:
        project = request.args.get('project', 'default')
        index_name = request.args.get('index_name', DEFAULT_INDEX_NAME)
        
        # Get index stats
        index = get_or_create_index(index_name)
        stats = index.describe_index_stats()
        
        # Get namespace stats
        namespace_stats = stats.namespaces.get(project, {})
        
        # Query for sample documents to get unique document IDs
        # This is a workaround since Pinecone doesn't have a direct "list all docs" API
        sample_results = index.query(
            vector=[0] * EMBEDDING_DIMENSION,
            top_k=10000,
            namespace=project,
            include_metadata=True
        )
        
        # Group by document_id
        documents = {}
        for match in sample_results.matches:
            doc_id = match.metadata.get('document_id')
            if doc_id not in documents:
                documents[doc_id] = {
                    'document_id': doc_id,
                    'filename': match.metadata.get('filename'),
                    'project': match.metadata.get('project'),
                    'upload_date': match.metadata.get('upload_date'),
                    'total_chunks': match.metadata.get('total_chunks', 0),
                    'file_size': match.metadata.get('file_size', 0)
                }
        
        documents_list = list(documents.values())
        documents_list.sort(key=lambda x: x.get('upload_date', ''), reverse=True)
        
        return jsonify({
            'success': True,
            'project': project,
            'documents': documents_list,
            'total_documents': len(documents_list),
            'total_vectors': namespace_stats.get('vector_count', 0)
        })
        
    except Exception as e:
        print(f"List documents error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/documents/<document_id>', methods=['DELETE'])
def delete_document(document_id):
    """Delete a document and all its chunks"""
    try:
        project = request.args.get('project', 'default')
        index_name = request.args.get('index_name', DEFAULT_INDEX_NAME)
        
        index = get_or_create_index(index_name)
        
        # Find all chunks for this document
        results = index.query(
            vector=[0] * EMBEDDING_DIMENSION,
            top_k=10000,
            namespace=project,
            include_metadata=True,
            filter={'document_id': document_id}
        )
        
        # Delete all chunks
        vector_ids = [match.id for match in results.matches]
        if vector_ids:
            index.delete(ids=vector_ids, namespace=project)
        
        return jsonify({
            'success': True,
            'document_id': document_id,
            'chunks_deleted': len(vector_ids)
        })
        
    except Exception as e:
        print(f"Delete error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        index_name = request.args.get('index_name', DEFAULT_INDEX_NAME)
        index = get_or_create_index(index_name)
        stats = index.describe_index_stats()
        
        return jsonify({
            'success': True,
            'total_vectors': stats.total_vector_count,
            'namespaces': {
                name: {
                    'vector_count': ns.vector_count
                }
                for name, ns in stats.namespaces.items()
            }
        })
        
    except Exception as e:
        print(f"Stats error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/indexes', methods=['GET'])
def list_indexes():
    """List all Pinecone indexes"""
    try:
        indexes = pc.list_indexes()
        index_list = []
        
        for index_info in indexes:
            index_list.append({
                'name': index_info.name,
                'dimension': index_info.dimension,
                'metric': index_info.metric,
                'host': index_info.host
            })
        
        return jsonify({
            'success': True,
            'indexes': index_list,
            'total_indexes': len(index_list)
        })
        
    except Exception as e:
        print(f"List indexes error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/indexes', methods=['POST'])
def create_index():
    """Create a new Pinecone index"""
    try:
        data = request.get_json()
        index_name = data.get('index_name', '').strip()
        
        if not index_name:
            return jsonify({'error': 'Index name is required'}), 400
        
        # Validate index name (alphanumeric and hyphens only)
        if not index_name.replace('-', '').replace('_', '').isalnum():
            return jsonify({'error': 'Index name must contain only alphanumeric characters, hyphens, and underscores'}), 400
        
        # Check if index already exists
        existing_indexes = [idx.name for idx in pc.list_indexes()]
        
        if index_name in existing_indexes:
            return jsonify({'error': f'Index "{index_name}" already exists'}), 400
        
        # Create the index
        pc.create_index(
            name=index_name,
            dimension=EMBEDDING_DIMENSION,
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region=PINECONE_ENVIRONMENT
            )
        )
        
        return jsonify({
            'success': True,
            'message': f'Index "{index_name}" created successfully',
            'index_name': index_name,
            'dimension': EMBEDDING_DIMENSION
        })
        
    except Exception as e:
        print(f"Create index error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/indexes/<index_name>', methods=['DELETE'])
def delete_index(index_name):
    """Delete a Pinecone index"""
    try:
        # Prevent deletion of default index
        if index_name == DEFAULT_INDEX_NAME:
            return jsonify({'error': f'Cannot delete default index "{DEFAULT_INDEX_NAME}"'}), 400
        
        # Check if index exists
        existing_indexes = [idx.name for idx in pc.list_indexes()]
        
        if index_name not in existing_indexes:
            return jsonify({'error': f'Index "{index_name}" does not exist'}), 404
        
        # Delete the index
        pc.delete_index(index_name)
        
        return jsonify({
            'success': True,
            'message': f'Index "{index_name}" deleted successfully',
            'index_name': index_name
        })
        
    except Exception as e:
        print(f"Delete index error: {traceback.format_exc()}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Get port from environment variable (required for Render)
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting server on port {port}...")
    app.run(debug=False, host='0.0.0.0', port=port)
