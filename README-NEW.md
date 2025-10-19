# 🚀 Knowledge Base Portal - Complete System

**AI-Powered Document Management with Pinecone & Google Gemini**

---

## ✨ What's New

This is a **complete rewrite** that replaces the n8n webhook system with:
- ✅ Direct Pinecone vector database integration
- ✅ Google Gemini AI for FREE embeddings
- ✅ Modern web interface with search capabilities
- ✅ Knowledge base browser and management
- ✅ Multi-project support (Mubest, Fortius)

## 🎯 Key Features

| Feature | Description |
|---------|-------------|
| **📤 Document Upload** | PDF, DOCX, TXT, Excel (XLSX, CSV) with drag & drop |
| **🔍 Semantic Search** | AI-powered search using Gemini embeddings |
| **📚 Knowledge Browser** | View all documents with stats and metadata |
| **🗑️ Document Management** | Delete documents and manage your knowledge base |
| **🎨 Beautiful UI** | Modern TailwindCSS interface with animations |
| **💰 100% FREE** | Uses Gemini's free tier (no OpenAI costs!) |

## 📂 File Structure

```
Rag data ingestion/
├── app.html                  # ⭐ NEW: Main web application
├── backend/
│   ├── app.py               # ⭐ NEW: Python Flask API server
│   ├── requirements.txt     # Python dependencies
│   ├── .env                 # ✅ Already configured with your keys
│   └── .env.example         # Template for future reference
├── QUICKSTART.md            # ⭐ Quick start guide (read this first!)
├── SETUP.md                 # Detailed setup documentation
├── start.sh                 # One-command startup script
└── index.html               # OLD: Original n8n version (kept for reference)
```

## ⚡ Quick Start (3 Steps)

### 1️⃣ Install Dependencies
```bash
cd backend
pip3 install -r requirements.txt
```

### 2️⃣ Start Server
```bash
./start.sh
```

### 3️⃣ Use the App
The browser will open automatically with `app.html`

## 🔑 Your Configuration

Your API keys are **already configured** in `backend/.env`:

| Service | Status |
|---------|--------|
| Pinecone | ✅ Configured |
| Google Gemini | ✅ Configured |

## 💡 How It Works

```
1. Upload Document → 2. Extract Text → 3. Chunk Text → 4. Generate Embeddings → 5. Store in Pinecone
                                                              ↓
                                               6. Search Query ← 7. Get Results ← User
```

### Technology Stack
- **Backend**: Python Flask + Pinecone + Google Gemini
- **Frontend**: HTML + TailwindCSS + Vanilla JavaScript
- **Vector DB**: Pinecone (serverless)
- **Embeddings**: Google Gemini (768-dimensional vectors)

## 📊 What You Can Do

### Upload Documents
- Select your project (Mubest or Fortius)
- Upload multiple files at once
- View real-time processing progress
- See chunk count and file statistics

### Search Knowledge Base
- Natural language queries
- Semantic similarity matching
- See relevance scores (0-100%)
- View matching text chunks with context

### Browse Documents
- View all uploaded documents
- See upload dates and file sizes
- Check total vectors and chunks
- Delete documents when needed

## 🆚 Comparison: Old vs New

| Feature | Old (index.html) | New (app.html) |
|---------|------------------|----------------|
| Backend | n8n webhook | Direct Python API |
| Search | ❌ No search | ✅ AI semantic search |
| Browse | ❌ No browsing | ✅ Full knowledge base browser |
| Embeddings | None | ✅ Gemini (FREE) |
| Vector DB | None | ✅ Pinecone |
| Management | ❌ No management | ✅ Delete, view stats |
| Cost | n8n subscription | 100% FREE |

## 💰 Pricing

| Service | Free Tier | Cost |
|---------|-----------|------|
| **Pinecone** | 100k vectors | $0/month |
| **Gemini** | 60 req/min | $0/month |
| **Total** | - | **$0/month** |

Perfect for small to medium knowledge bases!

## 🎓 Example Use Cases

1. **Company Knowledge Base**
   - Upload policies, procedures, handbooks
   - Search with natural language
   - Get instant answers

2. **Project Documentation**
   - Store project docs per client (Mubest, Fortius)
   - Quick semantic search
   - Track all documents

3. **Research Papers**
   - Upload academic papers
   - Find related content
   - Cross-reference documents

## 🔧 Advanced Configuration

### Add New Projects
Just add to the dropdown in `app.html` - namespaces are auto-created in Pinecone.

### Adjust Chunk Size
Edit `backend/app.py`:
```python
CHUNK_SIZE = 1000      # Characters per chunk
CHUNK_OVERLAP = 200    # Overlap between chunks
```

### Change Embedding Model
Currently using `models/embedding-001` (Gemini's best free model)

## 📖 Documentation

- **QUICKSTART.md** - Get started in 5 minutes
- **SETUP.md** - Detailed setup and configuration
- **This file** - Overview and comparison

## 🐛 Troubleshooting

**Backend won't start?**
```bash
cd backend
pip3 install --upgrade -r requirements.txt
python3 app.py
```

**CORS errors in browser?**
- Make sure backend is running on `http://localhost:5000`
- Check browser console for details

**No results when searching?**
- Make sure you've uploaded documents first
- Select the correct project

**API key errors?**
- Check `backend/.env` file exists
- Verify API keys are correct

## 🚀 Ready to Start?

Read **QUICKSTART.md** for a 5-minute guide to get up and running!

---

**Built with ❤️ using Pinecone, Gemini AI, and Flask**

*No more n8n webhooks - just pure, direct API integration!*
