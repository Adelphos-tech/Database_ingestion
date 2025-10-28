#!/usr/bin/env python3
"""
Test if captcha solving is properly configured
"""
import os
from dotenv import load_dotenv

print("🔍 Checking Captcha Bypass Configuration\n")
print("=" * 60)

# Load environment variables
load_dotenv('backend/.env')

# Check Railway environment (simulated)
railway_vars = {
    'ENABLE_PLAYWRIGHT_CRAWL': os.getenv('ENABLE_PLAYWRIGHT_CRAWL', 'NOT SET'),
    'TWOCAPTCHA_API_KEY': os.getenv('TWOCAPTCHA_API_KEY', 'NOT SET'),
    'ANTICAPTCHA_API_KEY': os.getenv('ANTICAPTCHA_API_KEY', 'NOT SET'),
    'CAPSOLVER_API_KEY': os.getenv('CAPSOLVER_API_KEY', 'NOT SET'),
}

print("\n📊 Environment Variables:")
print("-" * 60)
for key, value in railway_vars.items():
    if value and value != 'NOT SET' and 'API_KEY' in key:
        masked_value = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
        status = "✅" if value != 'NOT SET' else "❌"
        print(f"{status} {key}: {masked_value}")
    else:
        status = "✅" if value == 'true' else ("❌" if value == 'NOT SET' else "⚠️")
        print(f"{status} {key}: {value}")

print("\n" + "=" * 60)
print("\n📝 Analysis:")
print("-" * 60)

# Check Playwright
if railway_vars['ENABLE_PLAYWRIGHT_CRAWL'] == 'true':
    print("✅ Playwright crawling: ENABLED")
else:
    print("❌ Playwright crawling: DISABLED")
    print("   → Set ENABLE_PLAYWRIGHT_CRAWL=true")

# Check Captcha solving
captcha_services = []
if railway_vars['TWOCAPTCHA_API_KEY'] != 'NOT SET':
    captcha_services.append('2Captcha')
if railway_vars['ANTICAPTCHA_API_KEY'] != 'NOT SET':
    captcha_services.append('AntiCaptcha')
if railway_vars['CAPSOLVER_API_KEY'] != 'NOT SET':
    captcha_services.append('CapSolver')

print("\n🔐 Captcha Solving Services:")
if captcha_services:
    print(f"✅ Configured: {', '.join(captcha_services)}")
    print(f"   → {len(captcha_services)} service(s) available")
else:
    print("❌ NO captcha services configured!")
    print("   → Captcha bypass will NOT work")
    print("   → Get free API key from:")
    print("      • 2Captcha: https://2captcha.com (Free $3)")
    print("      • AntiCaptcha: https://anti-captcha.com (Free $1)")
    print("      • CapSolver: https://www.capsolver.com (Free $1)")

print("\n" + "=" * 60)
print("\n🎯 What This Means:")
print("-" * 60)

if railway_vars['ENABLE_PLAYWRIGHT_CRAWL'] != 'true':
    print("❌ Playwright disabled → Even simple bot detection will block you")
elif not captcha_services:
    print("⚠️  Playwright enabled BUT no captcha solving")
    print("   → Will work for sites WITHOUT captcha")
    print("   → Will FAIL on sites WITH captcha (PropertyGuru may have captcha)")
else:
    print("✅ Full bypass configured!")
    print("   → Playwright will launch")
    print("   → Captchas will be automatically solved")

print("\n" + "=" * 60)
print("\n💡 Quick Fix:")
print("-" * 60)

fixes_needed = []

if railway_vars['ENABLE_PLAYWRIGHT_CRAWL'] != 'true':
    fixes_needed.append("1. Set ENABLE_PLAYWRIGHT_CRAWL=true in Railway")

if not captcha_services:
    fixes_needed.append("2. Add at least one captcha API key:")
    fixes_needed.append("   → TWOCAPTCHA_API_KEY=your_key")
    fixes_needed.append("   → Get free key: https://2captcha.com")

if fixes_needed:
    for fix in fixes_needed:
        print(fix)
else:
    print("✅ Everything is configured correctly!")

print("\n" + "=" * 60)
print("\n🧪 Next Steps:")
print("-" * 60)
print("1. Fix any missing configuration above")
print("2. Redeploy on Railway (auto-redeploys on variable change)")
print("3. Wait 3-5 minutes for deployment")
print("4. Test: python3 test_crawl.py")
print("\n")
