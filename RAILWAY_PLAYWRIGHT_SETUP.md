# Enable Playwright Crawling on Railway

## Problem
PropertyGuru and similar protected sites return:
```
Error: No crawlable pages were found at the supplied URL.
```

## Root Cause
`ENABLE_PLAYWRIGHT_CRAWL` environment variable is not set to `true` in Railway deployment.

---

## ✅ Solution: Enable Playwright on Railway

### Step 1: Set Environment Variable

1. Go to **Railway Dashboard**: https://railway.app
2. Select your **Database_ingestion** project
3. Click on your **Backend service**
4. Go to **Variables** tab
5. Click **+ New Variable**
6. Add:
   ```
   Variable: ENABLE_PLAYWRIGHT_CRAWL
   Value: true
   ```
7. Click **Add** and **Deploy**

### Step 2: Verify Playwright Dependencies

Your `backend/requirements.txt` already has:
```
playwright
playwright-stealth
undetected-chromedriver
cloudscraper
```

### Step 3: Add Playwright Install Command

Railway needs to install Playwright browsers. Add to your deployment:

**Option A: Update `railway.toml`**
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "playwright install chromium && gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app"
```

**Option B: Create `nixpacks.toml`**
```toml
[phases.setup]
nixPkgs = ["python310", "chromium"]

[phases.install]
cmds = ["pip install -r backend/requirements.txt", "playwright install chromium"]

[start]
cmd = "gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app"
```

**Option C: Add to start.sh**
```bash
#!/bin/bash
playwright install chromium
gunicorn -w 4 -b 0.0.0.0:$PORT backend.app:app
```

---

## 🧪 Test After Deployment

Run this command to test:
```bash
python3 test_crawl.py
```

You should see:
```
✅ SUCCESS! Crawling works!
✅ Pages ingested: 1
```

---

## 📊 Check Logs

After setting `ENABLE_PLAYWRIGHT_CRAWL=true`, check Railway logs:

You should see these log messages when crawling:
```
Attempting to fetch: https://www.propertyguru.com.sg/...
✗ fetch_with_requests failed
✗ fetch_with_cloudscraper failed
✓ fetch_with_playwright succeeded  ← This should appear!
```

If you see:
```
✗ Playwright crawling disabled (ENABLE_PLAYWRIGHT_CRAWL=false)
```
Then the environment variable is not set correctly.

---

## 🔥 If Playwright Still Fails

### Option 1: Add Proxy
PropertyGuru may block Railway's IP. Add a proxy:

```bash
# In Railway Variables
PROXY_URL=http://username:password@proxy-server:port
```

### Option 2: Use Residential Proxies
For heavily protected sites:
- Oxylabs
- Bright Data
- Smartproxy

### Option 3: Try Different Approach
Instead of crawling, scrape manually:
1. Use browser extension to save HTML
2. Upload saved file to the chat interface
3. AI will analyze it the same way

---

## 💰 Cost Consideration

Playwright uses more resources (RAM, CPU):
- **Without Playwright**: ~512MB RAM
- **With Playwright**: ~1GB RAM (Chromium browser)

Railway charges based on usage - monitor your costs!

---

## ✅ Summary

1. ✅ Set `ENABLE_PLAYWRIGHT_CRAWL=true` in Railway Variables
2. ✅ Ensure Playwright browsers are installed (`playwright install chromium`)
3. ✅ Redeploy and test
4. ✅ Check logs for "fetch_with_playwright succeeded"
5. ✅ If still blocked, add proxy or use manual upload

**Test command:** `python3 test_crawl.py`
