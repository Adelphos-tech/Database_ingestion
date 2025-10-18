# Example n8n Workflow Configuration

This guide shows you how to set up your n8n workflow to process the chunked data from the portal and send it to Pinecone.

## Workflow Overview

```
Webhook → Process Chunks → Generate Embeddings → Upsert to Pinecone → Respond
```

## Node Configuration

### 1. Webhook Node

**Settings:**
- HTTP Method: `POST`
- Path: `/webhook-test/0a5bf047-9034-488b-87e5-0bb11cd0c058`
- Response Mode: `Using 'Respond to Webhook' Node`
- Authentication: None (or configure as needed)

**What it receives:**
```json
{
  "metadata": {...},
  "chunks": [...],
  "fullText": "..."
}
```

---

### 2. Code Node - "Process Chunks"

**Purpose:** Transform the chunks array into separate items for batch processing

**JavaScript Code:**
```javascript
// Extract chunks and metadata from the webhook payload
const chunks = $input.item.json.chunks;
const metadata = $input.item.json.metadata;

// Return each chunk as a separate item with metadata
return chunks.map(chunk => ({
  json: {
    text: chunk.text,
    chunkIndex: chunk.chunk_index,
    filename: metadata.filename,
    fileType: metadata.fileType,
    totalChunks: metadata.totalChunks,
    processedAt: metadata.processedAt
  }
}));
```

---

### 3. OpenAI Node - "Generate Embeddings"

**Settings:**
- Resource: `Embeddings`
- Model: `text-embedding-3-small` (or `text-embedding-ada-002`)
- Input: `{{ $json.text }}`

**Output:** Returns an embedding vector (array of numbers)

**Alternative: Cohere Node**
If using Cohere instead:
- Model: `embed-english-v3.0`
- Input Type: `search_document`

---

### 4. Code Node - "Prepare Pinecone Data"

**Purpose:** Format the data for Pinecone upsert

**JavaScript Code:**
```javascript
// Generate a unique ID for this chunk
const id = `${$json.filename}_chunk_${$json.chunkIndex}`;

// Get the embedding vector from OpenAI node
const embedding = $input.item.json.embedding;

// Prepare Pinecone upsert format
return {
  json: {
    id: id,
    values: embedding, // The vector
    metadata: {
      filename: $json.filename,
      fileType: $json.fileType,
      chunkIndex: $json.chunkIndex,
      totalChunks: $json.totalChunks,
      text: $json.text.substring(0, 1000), // Pinecone metadata limit
      processedAt: $json.processedAt
    }
  }
};
```

---

### 5. Pinecone Node - "Upsert Vectors"

**Settings:**
- Operation: `Upsert`
- Index: `your-index-name`
- Namespace: `documents` (optional)
- ID: `{{ $json.id }}`
- Values: `{{ $json.values }}`
- Metadata: `{{ $json.metadata }}`

**Credentials:**
- API Key: Your Pinecone API key
- Environment: Your Pinecone environment

---

### 6. Aggregate Node (Optional)

**Purpose:** Collect all results before responding

**Settings:**
- Aggregate: `All Items`
- Mode: `Combine All Items`

---

### 7. Respond to Webhook Node

**Settings:**
- Response Code: `200`
- Response Body:
```json
{
  "success": true,
  "message": "Successfully processed {{ $('Process Chunks').all().length }} chunks",
  "filename": "{{ $('Webhook').item.json.metadata.filename }}",
  "vectorsCreated": {{ $('Process Chunks').all().length }}
}
```

---

## Complete Workflow JSON

You can import this basic workflow structure:

```json
{
  "name": "Document Ingestion to Pinecone",
  "nodes": [
    {
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "position": [250, 300],
      "webhookId": "0a5bf047-9034-488b-87e5-0bb11cd0c058",
      "parameters": {
        "httpMethod": "POST",
        "path": "webhook-test/0a5bf047-9034-488b-87e5-0bb11cd0c058",
        "responseMode": "responseNode"
      }
    },
    {
      "name": "Process Chunks",
      "type": "n8n-nodes-base.code",
      "position": [450, 300],
      "parameters": {
        "jsCode": "// See JavaScript code above"
      }
    },
    {
      "name": "OpenAI Embeddings",
      "type": "n8n-nodes-base.openAi",
      "position": [650, 300],
      "parameters": {
        "resource": "embedding",
        "model": "text-embedding-3-small",
        "text": "={{ $json.text }}"
      }
    },
    {
      "name": "Prepare Pinecone",
      "type": "n8n-nodes-base.code",
      "position": [850, 300],
      "parameters": {
        "jsCode": "// See JavaScript code above"
      }
    },
    {
      "name": "Pinecone Upsert",
      "type": "@pinecone-database/n8n-nodes-pinecone.pinecone",
      "position": [1050, 300],
      "parameters": {
        "operation": "upsert",
        "index": "your-index-name"
      }
    },
    {
      "name": "Respond to Webhook",
      "type": "n8n-nodes-base.respondToWebhook",
      "position": [1250, 300],
      "parameters": {
        "respondWith": "json",
        "responseBody": "={{ { \"success\": true } }}"
      }
    }
  ],
  "connections": {
    "Webhook": { "main": [[{ "node": "Process Chunks", "type": "main", "index": 0 }]] },
    "Process Chunks": { "main": [[{ "node": "OpenAI Embeddings", "type": "main", "index": 0 }]] },
    "OpenAI Embeddings": { "main": [[{ "node": "Prepare Pinecone", "type": "main", "index": 0 }]] },
    "Prepare Pinecone": { "main": [[{ "node": "Pinecone Upsert", "type": "main", "index": 0 }]] },
    "Pinecone Upsert": { "main": [[{ "node": "Respond to Webhook", "type": "main", "index": 0 }]] }
  }
}
```

---

## Testing Your Workflow

### 1. Test the Webhook

Before using the portal, test your webhook with a sample payload:

```bash
curl -X POST https://personalgpt.app.n8n.cloud/webhook-test/0a5bf047-9034-488b-87e5-0bb11cd0c058 \
  -H "Content-Type: application/json" \
  -d '{
    "metadata": {
      "filename": "test.txt",
      "fileType": "txt",
      "totalChunks": 2,
      "totalCharacters": 1500,
      "processedAt": "2025-10-18T12:00:00Z"
    },
    "chunks": [
      {
        "text": "This is a test chunk.",
        "chunk_index": 0,
        "start_position": 0,
        "end_position": 21
      },
      {
        "text": "This is another test chunk.",
        "chunk_index": 1,
        "start_position": 21,
        "end_position": 48
      }
    ],
    "fullText": "This is a test chunk. This is another test chunk."
  }'
```

### 2. Check Pinecone

After successful execution:
1. Log into Pinecone console
2. Navigate to your index
3. Check the namespace `documents`
4. You should see vectors with IDs like `test.txt_chunk_0`, `test.txt_chunk_1`

### 3. Query Test

Test retrieval with Pinecone's query API to ensure vectors are searchable.

---

## Error Handling

Add an **Error Trigger** node to catch and log failures:

```javascript
// Error Handler Code Node
return {
  json: {
    error: true,
    message: $input.item.error.message,
    filename: $('Webhook').item.json.metadata?.filename,
    timestamp: new Date().toISOString()
  }
};
```

Connect this to a **Respond to Webhook** node with status 500.

---

## Optimization Tips

1. **Batch Processing**: Use n8n's "Split In Batches" node to process 10 chunks at a time
2. **Rate Limiting**: Add "Wait" nodes if you hit OpenAI rate limits
3. **Logging**: Add HTTP Request nodes to log to external services
4. **Retry Logic**: Enable automatic retries in n8n settings
5. **Caching**: Store full text in a database for re-processing with different chunk sizes

---

## Cost Estimation

For a 10-page PDF (~25,000 characters):
- Chunks: ~25 (at 1000 chars each)
- OpenAI Embeddings: $0.00001 per chunk = **$0.00025**
- Pinecone Storage: ~25 vectors = **~$0.001/month**

**Very cost-effective for most use cases!**
