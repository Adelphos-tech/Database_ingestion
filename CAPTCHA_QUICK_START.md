# Captcha Bypass - Quick Start

## 🚀 5-Minute Setup

### Step 1: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Configure Environment

Edit `backend/.env`:

```env
# Enable advanced crawling
ENABLE_PLAYWRIGHT_CRAWL=true

# Add at least one captcha service (get free trial credits)
TWOCAPTCHA_API_KEY=your_key_here

# Optional: Add proxy
PROXY_URL=http://your-proxy:8080
```

### Step 3: Start Server

```bash
cd backend
python app.py
```

### Step 4: Test It

```bash
curl -X POST http://localhost:5001/api/ingest-url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "project": "test",
    "max_pages": 3
  }'
```

## ✨ What You Get

| Feature | Status |
|---------|--------|
| **reCAPTCHA v2** | ✅ Auto-solved |
| **reCAPTCHA v3** | ✅ Auto-solved |
| **hCaptcha** | ✅ Auto-solved |
| **Cloudflare** | ✅ Auto-bypassed |
| **Bot Detection** | ✅ Avoided |
| **Proxy Support** | ✅ Available |

## 🔑 Get API Keys (Free Trials)

1. **2Captcha**: https://2captcha.com/enterpage
   - 💰 Get $0.50-$3 free credits
   
2. **AntiCaptcha**: https://anti-captcha.com/clients/entrance/register
   - 💰 Get $1 free credits
   
3. **CapSolver**: https://dashboard.capsolver.com/passport/register
   - 💰 Get $1 free credits

## 📊 How It Works

```
Your Request
    ↓
┌─────────────────────────────────────┐
│  1. Try Simple HTTP (fast)          │
│     ↓ (if blocked)                  │
│  2. Try Cloudscraper (Cloudflare)   │
│     ↓ (if captcha detected)         │
│  3. Launch Real Browser             │
│     ↓                               │
│  4. Detect Captcha Type             │
│     ↓                               │
│  5. Send to Solving Service         │
│     ↓                               │
│  6. Inject Solution                 │
│     ↓                               │
│  7. Get Page Content ✅             │
└─────────────────────────────────────┘
```

## 🎯 Supported Captcha Types

### reCAPTCHA v2 (Checkbox)
```
┌────────────────────────────┐
│ ☐ I'm not a robot          │
│                            │
│   [reCAPTCHA logo]         │
└────────────────────────────┘
```
**Detection**: Automatic  
**Solving**: 10-30 seconds  
**Cost**: ~$0.003 per solve

### reCAPTCHA v3 (Invisible)
```
(No visible UI - works in background)
```
**Detection**: Automatic  
**Solving**: 10-30 seconds  
**Cost**: ~$0.003 per solve

### hCaptcha
```
┌────────────────────────────┐
│ Please verify you are human│
│ [Click to verify]          │
└────────────────────────────┘
```
**Detection**: Automatic  
**Solving**: 15-45 seconds  
**Cost**: ~$0.002 per solve

## 🔧 Configuration Examples

### Minimal Setup (No Proxies)
```env
ENABLE_PLAYWRIGHT_CRAWL=true
TWOCAPTCHA_API_KEY=abc123
```

### With Single Proxy
```env
ENABLE_PLAYWRIGHT_CRAWL=true
TWOCAPTCHA_API_KEY=abc123
PROXY_URL=http://user:pass@proxy.com:8080
```

### With Rotating Proxies (Advanced)
```env
ENABLE_PLAYWRIGHT_CRAWL=true
TWOCAPTCHA_API_KEY=abc123
PROXY_ROTATION_ENABLED=true
PROXY_LIST=http://proxy1.com:8080,http://proxy2.com:8080,socks5://proxy3.com:1080
```

### Multiple Captcha Services (Redundancy)
```env
ENABLE_PLAYWRIGHT_CRAWL=true
TWOCAPTCHA_API_KEY=abc123
ANTICAPTCHA_API_KEY=def456
CAPSOLVER_API_KEY=ghi789
```

## 🧪 Test Sites

Try these to test your setup:

```bash
# Test 1: Simple site (should use requests)
curl -X POST http://localhost:5001/api/ingest-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "project": "test1"}'

# Test 2: JavaScript-heavy site (should use Playwright)
curl -X POST http://localhost:5001/api/ingest-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://spa-site.com", "project": "test2"}'

# Test 3: Protected site (will attempt captcha solving if detected)
curl -X POST http://localhost:5001/api/ingest-url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://protected-site.com", "project": "test3"}'
```

## 📈 Monitoring

Watch the logs to see what's happening:

```bash
python app.py
```

Look for these log messages:
- `✅ Google Gemini chat model configured`
- `Playwright fetch failed for...` (fallback to other methods)
- `reCAPTCHA v2 detected on...` (captcha found)
- `Attempting to solve reCAPTCHA v2...` (solving in progress)
- `reCAPTCHA v2 solved successfully` (captcha solved!)

## 💰 Cost Control

### Free Tier Strategy
1. Sign up for all 3 services (2Captcha, AntiCaptcha, CapSolver)
2. Get ~$5 total free credits
3. That's ~1,500-2,500 captcha solves!

### Budget Management
```python
# Estimate: 100 pages/day with 10% captcha rate
Daily captchas: 10
Daily cost: $0.03
Monthly cost: ~$0.90

# Heavy usage: 1,000 pages/day with 50% captcha rate
Daily captchas: 500
Daily cost: $1.50
Monthly cost: ~$45
```

## 🛡️ Anti-Detection Features

Your crawler now has:

✅ **WebDriver masking** - Sites can't detect Selenium/Playwright  
✅ **Real browser fingerprint** - Looks like Chrome on Windows  
✅ **Human-like behavior** - Random delays, natural mouse movements  
✅ **Realistic headers** - Modern Chrome user agent & headers  
✅ **Plugin simulation** - Fake plugins list  
✅ **Timezone/locale** - Consistent geolocation data  
✅ **Canvas fingerprinting resistance** - Randomized canvas  

## 🚨 Troubleshooting

### "sync_playwright is not available"
```bash
pip install playwright
playwright install chromium
```

### "2Captcha error: ERROR_WRONG_USER_KEY"
- Check your API key is correct
- Ensure it's added to `.env` file
- Verify you have credits remaining

### "Browser closed" / "Timeout"
- Increase server resources (RAM)
- Reduce `max_pages` parameter
- Check firewall/antivirus blocking browser

### "Proxy connection failed"
- Test proxy with: `curl -x http://proxy:port https://google.com`
- Check proxy credentials
- Try without proxy first

## 📚 Full Documentation

For complete details, see:
- `CAPTCHA_BYPASS_GUIDE.md` - Comprehensive guide
- `README.md` - General setup instructions
- `.env.example` - All configuration options

## 🎓 Learning Resources

### Understanding Captchas
- [How reCAPTCHA Works](https://developers.google.com/recaptcha)
- [hCaptcha Documentation](https://docs.hcaptcha.com)

### Captcha Services
- [2Captcha API Docs](https://2captcha.com/2captcha-api)
- [AntiCaptcha API Docs](https://anti-captcha.com/apidoc)
- [CapSolver API Docs](https://docs.capsolver.com)

### Web Scraping Best Practices
- Respect `robots.txt`
- Add delays between requests
- Use proxies responsibly
- Monitor API costs

## ⚡ Pro Tips

1. **Start small**: Test with `max_pages=3` first
2. **Monitor costs**: Check captcha service dashboard
3. **Use caching**: Don't re-crawl same pages
4. **Rotate everything**: User agents, proxies, timing
5. **Handle failures**: Some sites are impossible to scrape

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Get captcha API key (free trial)
3. ✅ Configure `.env`
4. ✅ Test on simple site
5. ✅ Try protected site
6. ✅ Monitor logs and costs
7. ✅ Scale up as needed

---

**Need Help?** Check the full guide: `CAPTCHA_BYPASS_GUIDE.md`
