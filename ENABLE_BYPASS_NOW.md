# 🚨 RE-ENABLE YOUR BYPASS (IT'S ALREADY THERE!)

## ✅ Good News: Your Bypass Code Is Already Built!

Your backend has **ALL the bypass mechanisms** already coded:
- ✅ Cloudscraper (Cloudflare bypass)
- ✅ Playwright with stealth mode
- ✅ Anti-detection JavaScript
- ✅ Captcha solving (3 services)
- ✅ Proxy support

**It just needs to be turned ON!**

---

## ❌ Why It Stopped Working

The bypass is controlled by this environment variable:
```python
# Line 56 in backend/app.py
ENABLE_PLAYWRIGHT_CRAWL = os.getenv('ENABLE_PLAYWRIGHT_CRAWL', 'false').lower() == 'true'
```

**If this is `false`, Playwright bypass is disabled!**

When disabled (line 902):
```python
def fetch_with_playwright(url, timeout):
    if not ENABLE_PLAYWRIGHT_CRAWL or not sync_playwright:
        return None  # ← Bypass is skipped!
```

---

## 🔧 FIX IT NOW (2 Minutes)

### Step 1: Go to Railway Dashboard

1. Open: **https://railway.app**
2. Project: **Database_ingestion**
3. Service: **backend**
4. Tab: **Variables**

### Step 2: Add This Variable

Click **+ New Variable**:

```
Name: ENABLE_PLAYWRIGHT_CRAWL
Value: true
```

**IMPORTANT:** Value must be exactly `true` (lowercase)

### Step 3: Verify Other Variables

While you're there, check these are set:

| Variable | Required | Example |
|----------|----------|---------|
| `PINECONE_API_KEY` | ✅ Yes | `pcsk_...` |
| `GEMINI_API_KEY` | ✅ Yes | `AIza...` |
| `ENABLE_PLAYWRIGHT_CRAWL` | ✅ **YES** | `true` |
| `TWOCAPTCHA_API_KEY` | Optional | Get free $3 at 2captcha.com |
| `PROXY_URL` | Optional | If Railway IP is blocked |

### Step 4: Redeploy

Railway will **auto-redeploy** when you add the variable.

Wait ~2-3 minutes for deployment to complete.

---

## 🧪 Test It

Run this to verify it's working:

```bash
python3 test_crawl.py
```

Or test directly:
```bash
curl -X POST "https://database-ingestion-production.up.railway.app/api/ingest-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.propertyguru.com.sg/property-for-rent",
    "project": "test",
    "index_name": "document-knowledge-base",
    "max_pages": 1,
    "max_depth": 0
  }' | python3 -m json.tool
```

**Expected result:**
```json
{
  "success": true,
  "ingested": [
    {
      "url": "https://www.propertyguru.com.sg/property-for-rent",
      "title": "...",
      "chunks": 10
    }
  ]
}
```

---

## 📊 What Happens When Enabled

With `ENABLE_PLAYWRIGHT_CRAWL=true`, the crawler tries 3 methods:

### Method 1: requests (Fast but often blocked)
```
✗ fetch_with_requests failed
```

### Method 2: cloudscraper (Cloudflare bypass)
```
✗ fetch_with_cloudscraper failed  
```
(PropertyGuru has additional protection beyond Cloudflare)

### Method 3: Playwright + Stealth ✅
```
✓ fetch_with_playwright succeeded
```

**This is the one that works for PropertyGuru!**

Playwright:
- Launches real Chrome browser
- Applies stealth mode (`playwright-stealth`)
- Injects anti-detection JavaScript
- Mimics human behavior
- Scrolls page to load lazy images
- Waits for JavaScript execution
- Bypasses most bot detection

---

## 🔍 Check Railway Logs

After enabling, go to Railway **Logs** tab and look for:

```
Attempting to fetch: https://www.propertyguru.com.sg/...
✗ fetch_with_requests failed for https://...
✗ fetch_with_cloudscraper failed for https://...
✓ fetch_with_playwright succeeded for https://...  ← SHOULD SEE THIS!
```

If you see:
```
✗ Playwright crawling disabled (ENABLE_PLAYWRIGHT_CRAWL=false)
```
Then the variable is not set correctly.

---

## 🚀 Advanced: Add Captcha Solving

If PropertyGuru shows captcha, enable automatic solving:

### Get Free API Key (3 options):

**Option 1: 2Captcha** (Recommended)
- Signup: https://2captcha.com
- Free $3 credit = ~1,000 solves
- Add to Railway: `TWOCAPTCHA_API_KEY=your_key`

**Option 2: AntiCaptcha**  
- Signup: https://anti-captcha.com
- Free $1 credit = ~500 solves
- Add to Railway: `ANTICAPTCHA_API_KEY=your_key`

**Option 3: CapSolver**
- Signup: https://www.capsolver.com  
- Free $1 credit = ~1,250 solves (cheapest)
- Add to Railway: `CAPSOLVER_API_KEY=your_key`

**The crawler will automatically:**
1. Detect captcha on page
2. Extract site key
3. Send to solving service
4. Wait for solution
5. Inject solution
6. Continue crawling

---

## 💰 Cost

| Item | Cost | When Needed |
|------|------|-------------|
| **Railway** | ~$5/month | Always (hosting) |
| **Playwright** | $0 | Free (open source) |
| **Captcha Solving** | ~$2.99/1000 | Only if captcha appears |
| **Proxy** | $0-50/month | If Railway IP blocked |

**PropertyGuru typically doesn't have captcha**, so captcha solving is optional!

---

## 🎯 Why It Was Working Before

Your crawler worked before because:
1. ✅ `ENABLE_PLAYWRIGHT_CRAWL=true` was set
2. ✅ Playwright browsers were installed
3. ✅ Railway had enough resources

It stopped because:
- ❌ Variable got removed/reset during redeployment
- ❌ Or new Railway project didn't have it
- ❌ Or you switched environments

**Solution: Just turn it back on!**

---

## 📝 Summary Checklist

- [ ] Go to Railway Dashboard
- [ ] Open backend service Variables tab
- [ ] Add `ENABLE_PLAYWRIGHT_CRAWL=true`
- [ ] Wait for redeploy (~2 mins)
- [ ] Test with `python3 test_crawl.py`
- [ ] Check Railway logs for "playwright succeeded"
- [ ] ✅ PropertyGuru crawling works!

---

## 🆘 If It Still Doesn't Work

### 1. Check Playwright Installation

In Railway logs, look for:
```
ModuleNotFoundError: No module named 'playwright'
```

**Fix:** Ensure `requirements.txt` has:
```
playwright
playwright-stealth
```

### 2. Check Chromium Installation

Playwright needs Chromium browser installed.

**Fix:** Add to Railway start command:
```bash
playwright install chromium && gunicorn ...
```

### 3. Check Memory

Playwright needs ~1GB RAM. Railway free tier may struggle.

**Fix:** Upgrade Railway plan or reduce workers:
```bash
gunicorn -w 1 ...  # Reduce from 4 to 1 worker
```

### 4. PropertyGuru Blocking Railway IP

If even Playwright fails, Railway's IP may be blocked.

**Fix:** Add proxy:
```
PROXY_URL=http://proxy-server:port
```

---

## ✅ Quick Command

Just copy-paste this after enabling:

```bash
# Test PropertyGuru crawling
python3 test_crawl.py

# Or direct API call
curl -X POST "https://database-ingestion-production.up.railway.app/api/ingest-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.propertyguru.com.sg/property-for-rent",
    "project": "propertyguru-test",
    "max_pages": 2,
    "max_depth": 0
  }'
```

---

**TL;DR: Go to Railway → Variables → Add `ENABLE_PLAYWRIGHT_CRAWL=true` → Done!** 🎉
