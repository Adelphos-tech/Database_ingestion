# n8n Document Ingestion Portal (V1 - Hybrid Mode)

A premium, intelligent document processing portal that extracts text and chunks documents **client-side**, then sends both the **original file** (for n8n's Default Data Loader) and **pre-processed chunks** to n8n for maximum flexibility.

> 🔧 **Getting "No Binary File Found" error?** See [`FIX-NO-BINARY-ERROR.md`](./FIX-NO-BINARY-ERROR.md) for the solution!

## 🎯 Features

### 🚀 Hybrid Processing Architecture
- **Client-Side Text Extraction**: PDF, DOCX, Excel, and TXT files processed in browser
- **Adjustable Chunking**: Interactive sliders to customize chunk size (500-3000 chars) and overlap (0-500 chars)
- **Smart Chunking**: Sentence-boundary detection for better context preservation
- **JSON Payload**: Sends structured, Pinecone-ready data to n8n
- **Secure**: API keys stay in n8n, not exposed in browser code
- **File Validation**: Client-side validation for file type, size (50MB max), and content
- **Auto-Retry**: Exponential backoff retry logic (up to 3 attempts) for failed uploads

### 💎 Premium UI/UX
- **Project Selector** dropdown to choose between Mubest and Fortius workflows
- **Chunking Settings Panel** with real-time adjustable sliders
- **File Details Display** showing file name, size, type, and estimated chunks
- **Modern gradient design** with smooth animations
- **Drag & Drop** support for intuitive file uploads
- **Real-time progress feedback** (Extracting → Chunking → Sending → Retry attempts)
- **Multi-file type support**: PDF, DOCX, Excel (.xlsx, .xls, .csv), TXT
- **Responsive design** for all devices
- **CDN-based libraries** (PDF.js, Mammoth.js, SheetJS)

## 🔄 How Hybrid Mode Works

### Processing Pipeline

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐      ┌──────────┐
│   Browser   │ ───> │    n8n       │ ───> │   OpenAI    │ ───> │ Pinecone │
│  (Extract   │      │  (Generate   │      │ Embeddings  │      │  Vector  │
│  & Chunk)   │      │   Vectors)   │      │     API     │      │    DB    │
└─────────────┘      └──────────────┘      └─────────────┘      └──────────┘
```

### What Happens Where

**🌐 In the Browser (Client-Side):**
1. User uploads a document
2. JavaScript extracts text using specialized libraries (PDF.js, Mammoth, SheetJS)
3. Text is chunked into 1000-character pieces with 200-char overlap
4. Creates multipart/form-data with:
   - Original file (binary) under `data` key
   - Pre-processed chunks as JSON string
5. Sends to n8n webhook

**⚙️ In n8n (Server-Side - You Choose):**

**Option A (Simple):**
1. Receives file at `$binary.data`
2. Default Data Loader extracts & chunks
3. Pinecone Vector Store generates embeddings & stores

**Option B (Advanced):**
1. Receives pre-processed chunks from `$json.body.jsonData`
2. Skips text extraction (already done!)
3. Iterates through chunks
4. Calls OpenAI/Cohere API to generate embeddings
5. Upserts vectors + metadata to Pinecone
6. Returns success response

### Why This Approach?

✅ **Best of Both Worlds**: Works with Default Data Loader AND custom processing  
✅ **Offloads Heavy Processing**: Text extraction happens in user's browser  
✅ **Secure API Keys**: OpenAI/Pinecone keys never exposed to client  
✅ **No "Binary File" Errors**: Sends file under `$binary.data` as expected  
✅ **Better UX**: Real-time progress feedback during extraction  
✅ **Flexible**: Use pre-processed chunks or let n8n re-chunk as needed  
✅ **Cost-Effective**: Reduces server processing time  
✅ **Compatible**: Works with Pinecone Vector Store, AI Agents, Document Loaders

## 📋 Supported File Formats

- **Excel**: .xlsx, .xls, .csv
- **PDF**: .pdf
- **Word**: .docx, .doc
- **Text**: .txt

## 🚀 Quick Start

### Option 1: Open Locally (Testing)

Simply double-click `index.html` to open it in your default browser. However, note that form submission may be blocked by CORS policies when testing locally.

### Option 2: Deploy to Web Server (Recommended)

#### Using Python (Simple HTTP Server)

```bash
# Navigate to the directory
cd "/Users/shivang/Desktop/Rag data ingestion"

# Python 3
python3 -m http.server 8000

# Then open: http://localhost:8000
```

#### Using Node.js (http-server)

```bash
# Install http-server globally (one time)
npm install -g http-server

# Navigate to the directory
cd "/Users/shivang/Desktop/Rag data ingestion"

# Start server
http-server -p 8000

# Then open: http://localhost:8000
```

#### Deploy to Hosting Services

Upload `index.html` to any of these services:

- **Netlify**: Drag and drop the file to [netlify.com/drop](https://app.netlify.com/drop)
- **Vercel**: Deploy via [vercel.com](https://vercel.com)
- **GitHub Pages**: Commit to a GitHub repo and enable Pages
- **AWS S3**: Upload to S3 bucket with static website hosting
- **Firebase Hosting**: Deploy using Firebase CLI

## ⚙️ Configuration

### Project Selector (Multi-Webhook Support)

The portal includes a dropdown that allows users to select between different projects, each triggering a different n8n webhook:

- **Mubest** → `https://personalgpt.app.n8n.cloud/webhook/0a5bf047-9034-488b-87e5-0bb11cd0c058`
- **Fortius** → `https://personalgpt.app.n8n.cloud/webhook/adf85e36-1db7-4ba9-a39f-8ffcbd1262c2`

### Adding More Projects

To add more projects to the dropdown, edit the JavaScript in `index.html`:

```javascript
// Find this section (around line 347)
const webhookUrls = {
    mubest: 'https://personalgpt.app.n8n.cloud/webhook/0a5bf047-9034-488b-87e5-0bb11cd0c058',
    fortius: 'https://personalgpt.app.n8n.cloud/webhook/adf85e36-1db7-4ba9-a39f-8ffcbd1262c2',
    // Add your new project:
    newproject: 'https://your-webhook-url-here'
};
```

Then add the option to the HTML dropdown:

```html
<select id="projectSelect" class="project-select" required>
    <option value="mubest">Mubest</option>
    <option value="fortius">Fortius</option>
    <option value="newproject">New Project</option>
</select>
```

## 📦 n8n Webhook Configuration

Your n8n workflow should be configured to:

1. **Accept POST requests** with `multipart/form-data` encoding
2. **Receive both binary file and JSON data:**
   - **`data`** - The original file (binary) for Default Data Loader node
   - **`file`** - Duplicate of the file (for compatibility)
   - **`jsonData`** - String containing JSON with pre-processed chunks
   - **`fileType`** - File extension (e.g., "pdf", "docx")
   - **`mimeType`** - MIME type

3. **The `jsonData` field contains** a stringified JSON with this structure:

```json
{
  "metadata": {
    "filename": "document.pdf",
    "fileType": "pdf",
    "mimeType": "application/pdf",
    "fileSize": 524288,
    "totalChunks": 25,
    "totalCharacters": 24567,
    "processedAt": "2025-10-18T14:47:23.456Z",
    "chunkSize": 1000,
    "chunkOverlap": 200
  },
  "chunks": [
    {
      "text": "This is the first chunk of text...",
      "start_position": 0,
      "end_position": 1000,
      "chunk_index": 0
    },
    {
      "text": "This is the second chunk...",
      "start_position": 800,
      "end_position": 1800,
      "chunk_index": 1
    }
  ],
  "fullText": "The complete extracted text..."
}
```

3. **Return appropriate HTTP status codes**:
   - `200-299`: Success (portal shows success message)
   - `400-599`: Error (portal shows error message)

## 🔧 n8n Workflow Options

You now have **TWO options** for your n8n workflow:

### Option 1: Use Default Data Loader (Recommended for your setup)

This is the **easiest approach** if you're using Pinecone Vector Store node:

```
1. Webhook Node
   ↓
2. Default Data Loader (New)
   - Reads binary from $binary.data
   - Automatically extracts text and chunks
   ↓
3. Pinecone Vector Store (New)
   - Automatically generates embeddings
   - Stores in Pinecone
   ↓
4. Respond to Webhook
```

**Configuration:**
- The portal sends the file under `$binary.data` - this is what the Default Data Loader expects
- The pre-processed chunks in `$json.body.jsonData` are available if you want to skip text extraction

### Option 2: Use Pre-Processed Chunks (Maximum Control)

```
1. Webhook Node
   ↓
2. Code Node (Parse jsonData)
   - Parse: JSON.parse($json.body.jsonData)
   ↓
3. Code Node (Split chunks into items)
   ↓
4. OpenAI Embeddings Node
   ↓
5. Pinecone Upsert Node
   ↓
6. Respond to Webhook
```

**Configuration:**
- Access chunks via: `JSON.parse($json.body.jsonData).chunks`
- Skip text extraction - it's already done in the browser!

### Accessing Data in n8n

**Binary File (for Default Data Loader):**
- `{{ $binary.data }}` - The original uploaded file
- `{{ $binary.file }}` - Alternative field name

**Form Fields:**
- `{{ $json.body.project }}` - Selected project (e.g., "mubest" or "fortius")
- `{{ $json.body.fileType }}` - File extension (e.g., "pdf")
- `{{ $json.body.mimeType }}` - MIME type
- `{{ $json.body.jsonData }}` - Stringified JSON with chunks

**Pre-Processed Data (parse jsonData first):**

In a Code node, parse the JSON:
```javascript
const data = JSON.parse($json.body.jsonData);
return { json: data };
```

Then access:
- `{{ $json.metadata.filename }}` - Original filename
- `{{ $json.metadata.totalChunks }}` - Number of chunks
- `{{ $json.chunks }}` - Array of all text chunks
- `{{ $json.chunks[0].text }}` - First chunk's text
- `{{ $json.fullText }}` - Complete extracted text

### Sample n8n Function Node

Process chunks before embedding:

```javascript
// Add metadata to each chunk
const chunks = $input.item.json.chunks;
const metadata = $input.item.json.metadata;

return chunks.map(chunk => ({
  json: {
    text: chunk.text,
    metadata: {
      filename: metadata.filename,
      fileType: metadata.fileType,
      chunkIndex: chunk.chunk_index,
      totalChunks: metadata.totalChunks
    }
  }
}));
```

## 🎨 Customization

### Adjust Chunk Size and Overlap

Edit the chunking configuration in the JavaScript section:

```javascript
// Chunking configuration (around line 298)
const CHUNK_SIZE = 1000; // characters per chunk (default: 1000)
const CHUNK_OVERLAP = 200; // overlap between chunks (default: 200)
```

**Recommendations:**
- **Small chunks (500-800)**: Better for precise retrieval, more API calls
- **Medium chunks (1000-1500)**: Balanced approach (recommended)
- **Large chunks (2000-3000)**: Better context, fewer API calls
- **Overlap (100-300)**: Prevents information loss at chunk boundaries

### Change Colors

Edit the CSS gradients in the `<style>` section:

```css
/* Main gradient background */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

/* To change to blue-green: */
background: linear-gradient(135deg, #00b4db 0%, #0083b0 100%);
```

### Modify File Type Restrictions

Update the `accept` attribute in the file input:

```html
<input type="file" accept=".pdf,.docx,.doc,.txt,.xlsx,.xls,.csv">
```

### Customize Processing Messages

Edit the `showStatus()` function calls in the form submission handler to change user-facing messages.

## 🔒 Security Considerations

- **HTTPS Required**: For production, always serve this page over HTTPS
- **Webhook Security**: The n8n webhook URL should be kept private or secured with:
  - Hard-to-guess URL (current implementation)
  - Header authentication in n8n
  - IP whitelisting if possible
- **File Size Limits**: Consider adding client-side file size validation
- **File Type Validation**: Additional server-side validation in n8n is recommended

## 📱 Browser Compatibility

Tested and working on:
- ✅ Chrome (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Edge (latest)

## 🛠️ Technical Implementation

### Technologies Used
- **PDF.js** (v3.11.174) - PDF text extraction
- **Mammoth.js** (v1.6.0) - DOCX text extraction  
- **SheetJS** (v0.18.5) - Excel/CSV text extraction
- **Vanilla JavaScript** - Text chunking and orchestration
- **Fetch API** - Sending JSON to n8n webhook

### Functional Requirements (Enhanced)
- ✅ Client-side text extraction (PDF, DOCX, Excel, TXT)
- ✅ Intelligent text chunking with overlap
- ✅ Single file upload with drag & drop
- ✅ POST HTTP method with JSON payload
- ✅ Configured with n8n webhook URL
- ✅ Multi-stage loading states (Extract → Chunk → Send)
- ✅ Success/Error feedback with detailed messages
- ✅ Sentence-boundary-aware chunking

### Non-Functional Requirements
- ✅ CDN-hosted libraries (no build step required)
- ✅ Premium, clean, minimal UI
- ✅ Cross-browser compatible (Chrome, Firefox, Safari, Edge)
- ✅ HTTPS-ready (when deployed properly)
- ✅ Secure (API keys stay in n8n, not browser)

## 📁 Project Files

- **`index.html`** - The main portal (sends binary file + pre-processed chunks)
- **`README.md`** - This documentation
- **`FIX-NO-BINARY-ERROR.md`** - ⚡ Quick fix for "No Binary File Found" error
- **`example-n8n-workflow.md`** - Complete n8n workflow setup guide with code samples
- **`test-sample.txt`** - Test file to verify your setup works

## 🚦 Quick Start Checklist

1. ✅ **Start the server**: `python3 -m http.server 8000`
2. ✅ **Configure n8n**: Follow `example-n8n-workflow.md` to set up your workflow
3. ✅ **Test with sample file**: Upload a small PDF or TXT file
4. ✅ **Check Pinecone**: Verify vectors are being created
5. ✅ **Deploy**: Host on Netlify, Vercel, or your preferred platform

## 📞 Support

For issues or questions:
1. Check the **browser console** for JavaScript errors
2. Verify the **n8n webhook** is active and responding (test with curl)
3. Check the **n8n execution log** for processing errors
4. Verify **Pinecone credentials** and index configuration
5. Test with a **simple TXT file** first before complex PDFs

## 💡 Next Steps

- **Add authentication**: Implement basic auth or API key validation
- **File size limits**: Add client-side validation for large files
- **Progress bars**: Show upload progress for better UX
- **Batch uploads**: Extend to support multiple files
- **History dashboard**: Track uploaded documents
- **Custom metadata**: Add fields for tags, categories, etc.

## 📄 License

Internal use only.
