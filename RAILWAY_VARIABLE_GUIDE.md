# 🚨 URGENT: Enable PropertyGuru Bypass in Railway

## ❌ Current Status (Tested Just Now)

```
Test Results:
✅ example.com: SUCCESS (endpoint works)
❌ PropertyGuru: FAILED (bypass disabled)

Error: "No crawlable pages were found at the supplied URL."
```

---

## ✅ The Fix (2 Minutes)

### Visual Step-by-Step Guide:

```
┌─────────────────────────────────────────────────────────┐
│ Step 1: Open Railway Dashboard                         │
│ 👉 https://railway.app/dashboard                       │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Step 2: Click on "Database_ingestion" Project          │
│                                                         │
│  [Projects]                                             │
│   └─ 📦 Database_ingestion  ← Click this               │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Step 3: Select "backend" Service                       │
│                                                         │
│  Services:                                              │
│   └─ backend  ← Click this                             │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Step 4: Go to "Variables" Tab                          │
│                                                         │
│  [Settings] [Variables] [Deployments] [Logs]           │
│              ↑ Click this                               │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Step 5: Click "+ New Variable" Button                  │
│                                                         │
│  [+ New Variable]  ← Click this                        │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Step 6: Add the Variable                               │
│                                                         │
│  Variable name:                                         │
│  ┌───────────────────────────────────────┐             │
│  │ ENABLE_PLAYWRIGHT_CRAWL               │             │
│  └───────────────────────────────────────┘             │
│                                                         │
│  Value:                                                 │
│  ┌───────────────────────────────────────┐             │
│  │ true                                   │             │
│  └───────────────────────────────────────┘             │
│                                                         │
│  [Add]  ← Click this                                   │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Step 7: Wait for Redeploy (2-3 minutes)                │
│                                                         │
│  Deploying...  🔄                                       │
│  Installing dependencies...                             │
│  Starting server...                                     │
│  ✅ Deployed successfully!                              │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│ Step 8: Test Again                                      │
│                                                         │
│  $ python3 test_crawl.py                               │
│                                                         │
│  Expected:                                              │
│  ✅ PropertyGuru: SUCCESS! 🎉                           │
└─────────────────────────────────────────────────────────┘
```

---

## 🔍 What This Does

### Before (Current State):
```python
# Line 902 in backend/app.py
if not ENABLE_PLAYWRIGHT_CRAWL:  # ← False, so returns None
    return None

# Result: Playwright bypass is SKIPPED
# PropertyGuru blocks all other methods
# Error: "No crawlable pages found"
```

### After (With Variable Set):
```python
# Line 902 in backend/app.py
if not ENABLE_PLAYWRIGHT_CRAWL:  # ← True, continues!
    return None

# Playwright launches:
# 1. Real Chrome browser
# 2. Stealth mode enabled
# 3. Anti-detection JS injected
# 4. Mimics human behavior
# 5. Bypasses bot detection
# ✅ PropertyGuru content retrieved!
```

---

## 📊 Bypass Flow Visualization

```
PropertyGuru Request
        │
        ▼
┌───────────────────────┐
│ Method 1: requests    │
│ Simple HTTP request   │
└───────────────────────┘
        │
        ▼
    ❌ BLOCKED (bot detected)
        │
        ▼
┌───────────────────────┐
│ Method 2: cloudscraper│
│ Cloudflare bypass     │
└───────────────────────┘
        │
        ▼
    ❌ BLOCKED (still detected)
        │
        ▼
┌───────────────────────┐
│ Method 3: Playwright  │ ← NEEDS TO BE ENABLED!
│ Full browser + stealth│
└───────────────────────┘
        │
        ▼
    ✅ SUCCESS! Bypass works!
        │
        ▼
 PropertyGuru content extracted
```

---

## 🎯 Quick Copy-Paste

**Variable Name:**
```
ENABLE_PLAYWRIGHT_CRAWL
```

**Variable Value:**
```
true
```

**⚠️ CRITICAL:** Value must be exactly `true` (lowercase, no quotes)

---

## 🧪 How to Test After Enabling

### Option 1: Test Script
```bash
python3 test_crawl.py
```

### Option 2: Direct API Call
```bash
curl -X POST "https://database-ingestion-production.up.railway.app/api/ingest-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.propertyguru.com.sg/property-for-rent",
    "project": "test",
    "max_pages": 1,
    "max_depth": 0
  }'
```

**Expected Success Response:**
```json
{
  "success": true,
  "ingested": [
    {
      "url": "https://www.propertyguru.com.sg/property-for-rent",
      "title": "Property For Rent in Singapore | PropertyGuru Singapore",
      "chunks": 15,
      "depth": 0
    }
  ],
  "total_chunks": 15,
  "skipped": 0
}
```

---

## 📋 Verification Checklist

After enabling, verify in Railway Logs:

- [ ] See: `Attempting to fetch: https://www.propertyguru.com.sg/...`
- [ ] See: `✗ fetch_with_requests failed`
- [ ] See: `✗ fetch_with_cloudscraper failed`
- [ ] See: `✓ fetch_with_playwright succeeded` ← This is the key!
- [ ] No error: `✗ Playwright crawling disabled`
- [ ] Test script shows: `✅ SUCCESS! Crawling works!`

---

## 🔗 Direct Links

- **Railway Dashboard**: https://railway.app/dashboard
- **2Captcha** (if you need captcha solving): https://2captcha.com
- **Playwright Docs**: https://playwright.dev/python/

---

## 💡 Why It Worked Before

Your crawling worked before because:
1. ✅ You had set `ENABLE_PLAYWRIGHT_CRAWL=true`
2. ✅ Playwright was installed and running
3. ✅ PropertyGuru bypass was active

It stopped because:
- Variable got removed/reset during Railway redeployment
- Or you're using a different Railway project
- Or environment was rebuilt without variables

**Setting it again will restore full functionality!**

---

## 🆘 Still Not Working?

If after setting the variable it still fails:

### Check 1: Verify Variable Is Set
In Railway Logs, you should NOT see:
```
✗ Playwright crawling disabled (ENABLE_PLAYWRIGHT_CRAWL=false)
```

### Check 2: Check Memory
Playwright needs ~1GB RAM. Check Railway metrics.

### Check 3: Add Captcha Solving (if needed)
If PropertyGuru shows captcha:
```
TWOCAPTCHA_API_KEY=your_key_here
```

### Check 4: Add Proxy (last resort)
If Railway IP is blocked:
```
PROXY_URL=http://proxy-server:port
```

---

## ✅ Summary

**What to do:**
1. Go to Railway → Variables
2. Add `ENABLE_PLAYWRIGHT_CRAWL=true`
3. Wait 2 minutes for redeploy
4. Run `python3 test_crawl.py`
5. ✅ PropertyGuru works!

**Time:** 2 minutes  
**Cost:** $0 (Playwright is free)  
**Difficulty:** Easy (just add one variable)

---

**👉 Go to Railway NOW: https://railway.app/dashboard**
