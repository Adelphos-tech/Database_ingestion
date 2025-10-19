# ⚠️ Gemini API Quota Exceeded

## Error Details

Your upload is failing because the **Gemini API free tier quota has been exceeded**.

### Error Message:
```
429 You exceeded your current quota
Quota exceeded for metric: generativelanguage.googleapis.com/embed_content_free_tier_requests
```

## Gemini Free Tier Limits

- **60 requests per minute**
- **1,500 requests per day**

It appears you've hit the daily limit.

## Solutions

### Option 1: Wait for Quota Reset ⏰
The quota resets every 24 hours. Wait until tomorrow and try again.

### Option 2: Upgrade Gemini API (Recommended) 💳
Pay-as-you-go pricing:
- **Very cheap**: ~$0.00025 per 1,000 embeddings
- Much higher limits
- Reliable for production use

**To upgrade:**
1. Go to [Google AI Studio](https://ai.google.dev)
2. Enable billing on your Google Cloud project
3. API key will automatically use paid tier

### Option 3: Switch to OpenAI Embeddings 🔄
More reliable for production, but costs more:
- **text-embedding-3-small**: $0.02 per 1M tokens
- No free tier limits
- Very stable

**To switch to OpenAI:**
1. Get OpenAI API key from [platform.openai.com](https://platform.openai.com)
2. Update `backend/app.py` to use OpenAI instead of Gemini
3. Update `.env` with OpenAI key

### Option 4: Use Sentence Transformers (FREE) 🆓
Run embeddings locally (no API needed):
- **Completely free**
- No rate limits
- Slower but reliable
- Good quality embeddings

## Quick Fix: Switch to OpenAI

I can update your code to use OpenAI embeddings instead. Would you like me to do this?

**Cost comparison for 1000 documents:**
- **Gemini Free**: $0 (but limited)
- **Gemini Paid**: ~$0.25
- **OpenAI**: ~$0.50
- **Local (Sentence Transformers)**: $0

## Current Status

❌ **Uploads will fail** until quota resets or you upgrade
✅ **Backend is running** fine
✅ **Pinecone is working** fine
❌ **Gemini embedding generation** is blocked

## What Happened?

You likely uploaded several documents earlier, and each document gets chunked into multiple pieces. Each chunk needs an embedding, which counts against your quota.

For example:
- 1 PDF document → ~20 chunks
- 20 chunks → 20 API calls to Gemini
- 75 documents = 1,500 API calls (daily limit reached)

## Recommendation

For production use, I recommend **switching to OpenAI** or **upgrading Gemini to paid tier**.

Would you like me to:
1. Switch the code to use OpenAI embeddings?
2. Switch to local Sentence Transformers (free)?
3. Keep Gemini and wait for quota reset?

Let me know your preference!
