# Knowledge Base Portal with Pinecone - Setup Guide

This application provides a complete document management system with AI-powered semantic search using Pinecone vector database and Google Gemini embeddings.

## Features

✅ **Upload Documents** - PDF, DOCX, TXT, Excel (XLSX, CSV)  
✅ **Semantic Search** - AI-powered search using embeddings  
✅ **Browse Knowledge Base** - View all uploaded documents  
✅ **Multi-Project Support** - Separate namespaces for different projects  
✅ **Direct Pinecone Integration** - No n8n required  

## Prerequisites

1. **Python 3.8+** installed
2. **Pinecone Account** - Sign up at [pinecone.io](https://www.pinecone.io)
3. **Google Gemini API Key** - Get from [ai.google.dev](https://ai.google.dev)

## Installation Steps

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the `backend` directory:

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add your API keys:

```env
PINECONE_API_KEY=your_pinecone_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
PINECONE_ENVIRONMENT=us-east-1
```

**How to get your keys:**

- **Pinecone API Key**: 
  1. Go to [app.pinecone.io](https://app.pinecone.io)
  2. Create account or login
  3. Go to "API Keys" section
  4. Copy your API key

- **Google Gemini API Key**:
  1. Go to [ai.google.dev](https://ai.google.dev)
  2. Click "Get API Key in Google AI Studio"
  3. Create new API key
  4. Copy the key

### 3. Start the Backend Server

```bash
cd backend
python app.py
```

The backend will start on `http://localhost:5000`

### 4. Open the Frontend

Open `app.html` in your web browser:

```bash
# On Mac:
open app.html

# Or manually open in browser at:
file:///Users/shivang/Desktop/Rag%20data%20ingestion/app.html
```

## Usage

### Upload Documents

1. Click **"📤 Upload Documents"** tab
2. Select your project (Mubest or Fortius)
3. Drag & drop files or click to select
4. Click **"Upload to Knowledge Base"**
5. Wait for processing (text extraction → chunking → embedding → indexing)

### Browse Knowledge Base

1. Click **"📚 Browse Knowledge Base"** tab
2. Select your project
3. View all uploaded documents with statistics
4. Delete documents as needed

### Semantic Search

1. Click **"🔍 Semantic Search"** tab
2. Select your project
3. Enter your search query
4. View results ranked by semantic similarity

## API Endpoints

### Health Check
```
GET /health
```

### Upload Document
```
POST /api/upload
Body: multipart/form-data
- file: document file
- project: project name
```

### Search Documents
```
POST /api/search
Body: application/json
{
  "query": "your search query",
  "project": "project name",
  "top_k": 10
}
```

### List Documents
```
GET /api/documents?project=project_name
```

### Delete Document
```
DELETE /api/documents/{document_id}?project=project_name
```

### Get Statistics
```
GET /api/stats
```

## Project Structure

```
Rag data ingestion/
├── backend/
│   ├── app.py              # Flask backend server
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment variables (create this)
│   └── .env.example       # Environment template
├── app.html               # Main frontend application
├── index.html             # Old version (with n8n)
└── SETUP.md              # This file
```

## Troubleshooting

### Issue: "PINECONE_API_KEY not configured"
- Make sure you created `.env` file in backend directory
- Check that API keys are correctly set

### Issue: "CORS Error"
- Backend must be running on port 5000
- Check browser console for detailed errors

### Issue: "No text extracted"
- File might be corrupted or empty
- Some PDFs with images only won't work (needs OCR)

### Issue: "Gemini API Error"
- Check API key is valid
- Gemini API is free for moderate usage

## Configuration

### Change Chunk Size
Edit `backend/app.py`:
```python
CHUNK_SIZE = 1000      # Characters per chunk
CHUNK_OVERLAP = 200    # Overlap between chunks
```

### Change Embedding Model
Edit `backend/app.py`:
```python
EMBEDDING_MODEL = "models/embedding-001"  # Gemini embedding model
EMBEDDING_DIMENSION = 768  # Must match Gemini's output dimension
```

### Add New Project
Just use a new project name in the dropdown - namespaces are created automatically in Pinecone.

## Costs

- **Pinecone**: Free tier includes 1 index with up to 100k vectors (serverless)
- **Google Gemini**: FREE for up to 60 requests per minute

Example: A 100-page PDF (~50k words) can be embedded for **FREE** using Gemini API.

## Next Steps

1. Add authentication for production use
2. Implement batch uploads for faster processing
3. Add document preview functionality
4. Export search results to CSV
5. Add filters (date range, file type, etc.)

## Support

For issues or questions:
- Check Pinecone documentation: [docs.pinecone.io](https://docs.pinecone.io)
- Check Gemini documentation: [ai.google.dev/docs](https://ai.google.dev/docs)
