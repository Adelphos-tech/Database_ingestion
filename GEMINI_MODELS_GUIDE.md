# Gemini Models Guide

## Available Models

### 🚀 **gemini-2.5-flash-live** (Latest - Recommended)
```env
GEMINI_CHAT_MODEL=models/gemini-2.5-flash-live
```

**Best for:**
- ✅ Real-time chat streaming
- ✅ Instant responses
- ✅ Lowest latency
- ✅ Live conversations
- ✅ Most advanced features

**Features:**
- Latest Gemini 2.5 architecture
- Enhanced streaming (token-by-token)
- Improved context understanding
- Better reasoning capabilities
- Optimized for interactive chat
- Best user experience

---

### 🚀 **gemini-2.0-flash-live** (Stable)
```env
GEMINI_CHAT_MODEL=models/gemini-2.0-flash-live
```

**Best for:**
- ✅ Real-time chat streaming
- ✅ Instant responses
- ✅ Low latency
- ✅ Live conversations

**Features:**
- Streaming responses (token-by-token)
- Optimized for interactive chat
- Fast context switching
- Proven stability

---

### ⚡ **gemini-2.0-flash-exp** (Experimental)
```env
GEMINI_CHAT_MODEL=models/gemini-2.0-flash-exp
```

**Best for:**
- Testing new features
- Early access to capabilities
- Experimental features

**Features:**
- Latest experimental features
- May have instabilities
- Faster than 1.5 models

---

### 🧠 **gemini-1.5-pro** (Most Capable)
```env
GEMINI_CHAT_MODEL=models/gemini-1.5-pro
```

**Best for:**
- Complex reasoning
- Long documents
- Detailed analysis
- High accuracy requirements

**Features:**
- Best reasoning capabilities
- Largest context window (2M tokens)
- Slowest but most accurate
- Higher cost per request

---

### ⚡ **gemini-1.5-flash** (Balanced)
```env
GEMINI_CHAT_MODEL=models/gemini-1.5-flash
```

**Best for:**
- General purpose
- Production use
- Stable performance

**Features:**
- Good speed/quality balance
- Stable and reliable
- Lower cost than Pro

---

## How to Switch Models

### **Method 1: Environment Variable**

1. Edit your `.env` file:
```bash
cd backend
nano .env
```

2. Change the model:
```env
GEMINI_CHAT_MODEL=models/gemini-2.0-flash-live
```

3. Restart the server:
```bash
python app.py
```

---

### **Method 2: Railway Environment Variable**

1. Go to Railway dashboard
2. Click your project → **Variables**
3. Add/Update:
   - **Key**: `GEMINI_CHAT_MODEL`
   - **Value**: `models/gemini-2.0-flash-live`
4. Redeploy automatically

---

## Performance Comparison

| Model | Speed | Quality | Cost | Streaming |
|-------|-------|---------|------|-----------|
| **gemini-2.0-flash-live** | ⚡⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 | ✅ Best |
| **gemini-2.0-flash-exp** | ⚡⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 | ✅ Good |
| **gemini-1.5-flash** | ⚡⚡⚡ | ⭐⭐⭐⭐ | 💰 | ✅ Good |
| **gemini-1.5-pro** | ⚡⚡ | ⭐⭐⭐⭐⭐ | 💰💰💰 | ✅ Good |

---

## Use Cases

### **Use gemini-2.0-flash-live when:**
- 🎯 Building chat interfaces
- 🎯 Need instant feedback
- 🎯 Real-time Q&A
- 🎯 Interactive applications
- 🎯 User-facing chat

### **Use gemini-1.5-pro when:**
- 🎯 Complex document analysis
- 🎯 Deep reasoning required
- 🎯 Long context processing
- 🎯 High accuracy critical
- 🎯 Batch processing

### **Use gemini-1.5-flash when:**
- 🎯 Production stability needed
- 🎯 General purpose tasks
- 🎯 Cost optimization
- 🎯 Reliable performance

---

## API Limits

### Gemini 2.0 Flash Live
- **Free tier**: 15 RPM (requests per minute)
- **Free tier**: 1M TPM (tokens per minute)
- **Paid tier**: 1000 RPM
- **Paid tier**: 4M TPM

### Gemini 1.5 Pro
- **Free tier**: 2 RPM
- **Free tier**: 32K TPM
- **Paid tier**: 1000 RPM
- **Paid tier**: 4M TPM

---

## Example Configuration

**For maximum performance (your setup):**
```env
# .env
GEMINI_API_KEY=your_api_key_here
GEMINI_CHAT_MODEL=models/gemini-2.0-flash-live

# Railway Variables
GEMINI_CHAT_MODEL=models/gemini-2.0-flash-live
```

**Verification:**
```bash
# Check which model is active
cd backend
python3 -c "from app import CONFIGURED_CHAT_MODEL; print(f'Active model: {CONFIGURED_CHAT_MODEL}')"
```

---

## Streaming Example

The live model automatically streams responses token-by-token:

```python
# This happens automatically in your app
model = genai.GenerativeModel(CONFIGURED_CHAT_MODEL)
response = model.generate_content(prompt, stream=True)

for chunk in response:
    print(chunk.text, end='', flush=True)  # Real-time streaming
```

---

## Troubleshooting

### **Error: Model not found**
```
Solution: Check model name format
✅ models/gemini-2.0-flash-live
❌ gemini-2.0-flash-live (missing 'models/' prefix)
```

### **Error: Quota exceeded**
```
Solution: Switch to lower RPM model or upgrade to paid tier
GEMINI_CHAT_MODEL=models/gemini-1.5-flash
```

### **Slow responses**
```
Solution: Use faster model
GEMINI_CHAT_MODEL=models/gemini-2.0-flash-live
```

---

## Current Default

Your system is now configured to use:
```
✅ models/gemini-2.0-flash-live
```

This provides the best real-time chat experience! 🚀
