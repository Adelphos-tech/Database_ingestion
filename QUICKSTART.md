# Quick Start Guide

Your API keys are already configured! Follow these simple steps:

## 1. Install Dependencies

```bash
cd backend
pip3 install -r requirements.txt
```

## 2. Start the Server

```bash
# From the project root directory:
./start.sh

# OR manually:
cd backend
python3 app.py
```

## 3. Access the Application

The frontend will automatically open in your browser, or manually open:
- **File**: `app.html` 
- **URL**: `file:///Users/shivang/Desktop/Rag%20data%20ingestion/app.html`

## 4. Start Using!

### Upload Documents
1. Select "Mubest" or "Fortius" project
2. Drag & drop your files (PDF, DOCX, TXT, Excel)
3. Click "Upload to Knowledge Base"
4. Wait for processing to complete

### Search Documents
1. Go to "🔍 Semantic Search" tab
2. Enter your query (e.g., "What is the pricing model?")
3. View results ranked by relevance

### Browse Documents
1. Go to "📚 Browse Knowledge Base" tab
2. View all uploaded documents
3. See statistics and manage files

## Configured API Keys

✅ **Pinecone**: pcsk_65GWz3_GUoKLuRJcEqDWa1qAFkaNm3q7bGrTktvRruTqkWdC4j9J6f32wwVmNrejJmuYZG
✅ **Gemini**: AIzaSyAhLpo-Z_LUrjXUrxOFCprnXeMj9F0gksU

## Benefits of Using Gemini

🎉 **FREE** - No cost for embeddings (60 requests/min free)
⚡ **Fast** - High-quality embeddings at 768 dimensions
🎯 **Accurate** - Optimized for retrieval tasks

## Test Commands

### Check if backend is running:
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "pinecone_configured": true,
  "gemini_configured": true
}
```

## Troubleshooting

**Backend won't start?**
```bash
cd backend
pip3 install --upgrade -r requirements.txt
python3 app.py
```

**Can't access app.html?**
```bash
open app.html
# Or drag app.html into your browser
```

**Need to see backend logs?**
- Check the terminal where `python3 app.py` is running
- Look for error messages

## Next Steps

1. Upload a test document
2. Try searching for content
3. Browse your knowledge base
4. See the stats dashboard

Enjoy your AI-powered knowledge base! 🚀
