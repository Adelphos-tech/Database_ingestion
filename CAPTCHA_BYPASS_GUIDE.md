# Advanced Captcha Bypass Guide

This guide explains how to use the enhanced crawler with captcha bypass capabilities.

## Overview

The crawler now supports **automatic captcha detection and solving** with multiple layers of protection:

### Supported Captcha Types
- ✅ **reCAPTCHA v2** (checkbox captcha)
- ✅ **reCAPTCHA v3** (invisible captcha)
- ✅ **hCaptcha** (privacy-focused captcha)
- ✅ **Cloudflare Challenge** (via cloudscraper)

### Anti-Detection Features
- 🛡️ **Stealth mode** - Hides automation detection
- 🎭 **Browser fingerprinting** - Mimics real browsers
- 🌐 **Proxy rotation** - Rotates IP addresses
- 🔄 **User-agent rotation** - Multiple realistic user agents
- ⏱️ **Human-like delays** - Random timing patterns
- 📊 **WebDriver masking** - Removes automation signatures

## Quick Start

### 1. Enable Playwright Crawling

Add to your `.env` file:

```env
ENABLE_PLAYWRIGHT_CRAWL=true
```

### 2. Choose a Captcha Solving Service

Select one or more services (optional but recommended):

#### Option A: 2Captcha (Recommended)
```env
TWOCAPTCHA_API_KEY=your_2captcha_api_key
```
- **Website**: https://2captcha.com
- **Pricing**: ~$2.99 per 1000 captchas
- **Speed**: 10-30 seconds
- **Accuracy**: 95%+

#### Option B: AntiCaptcha
```env
ANTICAPTCHA_API_KEY=your_anticaptcha_api_key
```
- **Website**: https://anti-captcha.com
- **Pricing**: ~$2.00 per 1000 captchas
- **Speed**: 15-45 seconds
- **Accuracy**: 90%+

#### Option C: CapSolver
```env
CAPSOLVER_API_KEY=your_capsolver_api_key
```
- **Website**: https://www.capsolver.com
- **Pricing**: ~$0.80 per 1000 captchas
- **Speed**: 10-60 seconds
- **Accuracy**: 85%+

### 3. Configure Proxies (Optional)

#### Single Proxy
```env
PROXY_URL=http://username:password@proxy.example.com:8080
```

#### Proxy Rotation
```env
PROXY_ROTATION_ENABLED=true
PROXY_LIST=http://proxy1.com:8080,http://proxy2.com:8080,socks5://proxy3.com:1080
```

**Supported formats:**
- `http://host:port`
- `https://host:port`
- `socks5://host:port`
- `http://username:password@host:port`

## Installation

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install Playwright Browsers

```bash
playwright install chromium
```

This downloads the Chromium browser used for crawling.

## How It Works

### Crawling Strategy

The crawler uses a **multi-layered approach** with automatic fallback:

```
1. requests → Fast, simple HTTP requests
   ↓ (if fails)
2. cloudscraper → Cloudflare bypass
   ↓ (if fails)
3. Playwright → Full browser automation with captcha solving
```

### Captcha Detection & Solving Process

When Playwright is enabled:

1. **Page loads** with anti-detection measures
2. **Automatic captcha detection**:
   - Scans DOM for reCAPTCHA iframes
   - Detects hCaptcha elements
   - Identifies reCAPTCHA v3 scripts
3. **Site key extraction** from iframe/script sources
4. **Submit to solving service** (2Captcha/AntiCaptcha/CapSolver)
5. **Wait for solution** (10-60 seconds)
6. **Inject solution** into page
7. **Trigger callbacks** to submit captcha
8. **Continue crawling** with solved captcha

### Anti-Detection Techniques

The crawler implements multiple evasion techniques:

#### JavaScript Overrides
```javascript
// Hides webdriver property
navigator.webdriver = undefined

// Realistic plugins
navigator.plugins = [1, 2, 3, 4, 5]

// Chrome runtime object
window.chrome = { runtime: {} }
```

#### Browser Arguments
- `--disable-blink-features=AutomationControlled`
- `--disable-dev-shm-usage`
- `--no-sandbox`
- `--window-size=1920,1080`

#### Realistic Context
- **Viewport**: 1920x1080
- **Timezone**: America/New_York
- **Locale**: en-US
- **Geolocation**: New York coordinates
- **Device scale**: 1 (desktop)

## Usage Examples

### Example 1: Basic URL Crawl with Captcha Support

```bash
curl -X POST http://localhost:5001/api/ingest-url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "project": "my-project",
    "max_pages": 10,
    "max_depth": 2
  }'
```

### Example 2: Crawl Protected Website

```python
import requests

response = requests.post('http://localhost:5001/api/ingest-url', json={
    'url': 'https://protected-site.com',
    'project': 'protected-project',
    'max_pages': 5,
    'max_depth': 1
})

print(response.json())
```

### Example 3: Using with n8n

In your n8n workflow:

1. **HTTP Request Node**
   - Method: POST
   - URL: `http://your-server:5001/api/ingest-url`
   - Body:
     ```json
     {
       "url": "{{ $json.url }}",
       "project": "n8n-crawl",
       "max_pages": 10
     }
     ```

## Configuration Reference

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ENABLE_PLAYWRIGHT_CRAWL` | No | `false` | Enable browser automation |
| `TWOCAPTCHA_API_KEY` | No | - | 2Captcha API key |
| `ANTICAPTCHA_API_KEY` | No | - | AntiCaptcha API key |
| `CAPSOLVER_API_KEY` | No | - | CapSolver API key |
| `PROXY_URL` | No | - | Single proxy URL |
| `PROXY_ROTATION_ENABLED` | No | `false` | Enable proxy rotation |
| `PROXY_LIST` | No | - | Comma-separated proxy list |

### API Parameters

**POST `/api/ingest-url`**

```json
{
  "url": "string (required)",
  "project": "string (default: 'default')",
  "index_name": "string (default: 'document-knowledge-base')",
  "max_pages": "number (default: 5, max: 25)",
  "max_depth": "number (default: 1, max: 3)"
}
```

## Troubleshooting

### Common Issues

#### 1. Playwright Not Working

**Error**: `sync_playwright is not available`

**Solution**:
```bash
pip install playwright
playwright install chromium
```

#### 2. Captcha Not Solving

**Check**:
- API key is correct and has credits
- Network allows outbound connections to captcha service
- Site key is being extracted correctly (check logs)

**Enable debug logging**:
```python
import logging
logging.basicConfig(level=logging.INFO)
```

#### 3. Proxy Connection Failed

**Check**:
- Proxy format is correct
- Proxy credentials are valid
- Proxy server is online
- Firewall allows proxy connections

**Test proxy**:
```bash
curl -x http://proxy:port https://api.ipify.org
```

#### 4. Browser Launch Failed

**Error**: `Browser closed` or `Timeout`

**Solutions**:
- Increase timeout in code
- Check system resources (RAM/CPU)
- Install required system dependencies

**Linux dependencies**:
```bash
apt-get install -y \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2
```

### Debug Mode

Enable detailed logging to diagnose issues:

```python
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Performance Considerations

### Speed vs. Stealth Trade-offs

| Method | Speed | Stealth | Captcha Support | Use Case |
|--------|-------|---------|-----------------|----------|
| requests | ⚡⚡⚡ | ⭐ | ❌ | Simple sites |
| cloudscraper | ⚡⚡ | ⭐⭐⭐ | Limited | Cloudflare sites |
| Playwright | ⚡ | ⭐⭐⭐⭐⭐ | ✅ | Protected sites |

### Resource Usage

**Playwright crawling**:
- **Memory**: ~200-500MB per browser instance
- **CPU**: Moderate (JS execution)
- **Time**: 5-60 seconds per page (depending on captcha)

**Recommendations**:
- Limit concurrent crawls on low-memory systems
- Use `max_pages` and `max_depth` wisely
- Consider using a dedicated crawling server

## Best Practices

### 1. Respect robots.txt
Always check and respect the site's `robots.txt`:
```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("https://example.com/robots.txt")
rp.read()
can_fetch = rp.can_fetch("*", "https://example.com/page")
```

### 2. Rate Limiting
Add delays between requests:
```python
import time
time.sleep(2)  # 2 second delay
```

### 3. Rotating Resources
- Rotate user agents
- Rotate proxies
- Vary request patterns

### 4. Error Handling
- Implement retry logic
- Log failed URLs
- Handle timeouts gracefully

### 5. Cost Management
Captcha solving costs money:
- Cache solved pages
- Only solve when necessary
- Monitor usage and costs

## Security & Legal Considerations

### ⚠️ Important Warnings

1. **Legal Compliance**
   - Check site's Terms of Service
   - Respect copyright and data protection laws
   - Some jurisdictions have anti-scraping laws

2. **Ethical Use**
   - Don't overload servers
   - Don't bypass security for malicious purposes
   - Respect rate limits

3. **API Key Security**
   - Never commit API keys to version control
   - Use environment variables
   - Rotate keys periodically

4. **Proxy Usage**
   - Only use legitimate proxy services
   - Avoid free/public proxies (security risk)
   - Ensure compliance with proxy provider's terms

## Advanced Configuration

### Custom Captcha Solving Service

To add a custom service, extend the `CaptchaSolver` class:

```python
class CaptchaSolver:
    @staticmethod
    def _solve_custom_service(site_key, page_url, api_key):
        # Your implementation
        pass
```

### Custom Anti-Detection Script

Add custom JavaScript to Playwright:

```python
page.add_init_script("""
    // Your custom anti-detection code
    Object.defineProperty(navigator, 'hardwareConcurrency', {
        get: () => 4
    });
""")
```

## Cost Estimation

### Captcha Solving Costs

**Average website** (100 pages):
- Without captchas: $0
- 10% pages with captcha: ~$0.03
- 50% pages with captcha: ~$0.15
- 100% pages with captcha: ~$0.30

**Monthly crawling** (10,000 pages):
- 2Captcha: $3-30/month
- AntiCaptcha: $2-20/month
- CapSolver: $0.80-8/month

### Proxy Costs

**Residential proxies** (more reliable):
- $50-200/month for 5-40GB

**Datacenter proxies** (cheaper):
- $20-50/month for unlimited

## Support

For issues or questions:
- Check logs in the terminal
- Review this documentation
- Check captcha service status pages
- Test with simple sites first

## Changelog

### v2.0.0 - Advanced Captcha Bypass
- ✅ Added reCAPTCHA v2/v3 support
- ✅ Added hCaptcha support
- ✅ Integrated 2Captcha, AntiCaptcha, CapSolver
- ✅ Enhanced anti-detection measures
- ✅ Added proxy rotation support
- ✅ Improved browser fingerprinting
- ✅ Added playwright-stealth integration

### v1.0.0 - Basic Crawler
- ✅ Basic requests crawling
- ✅ Cloudscraper integration
- ✅ Playwright support
