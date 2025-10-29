"""
Test Custom Captcha Bypass with PropertyGuru
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import logging
from playwright.sync_api import sync_playwright
from captcha_bypass import CustomCaptchaBypass

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_propertyguru():
    """Test PropertyGuru.com.sg with custom bypass"""
    url = "https://www.propertyguru.com.sg/property-for-rent"
    
    print("\n" + "="*60)
    print("🧪 Testing Custom Captcha Bypass")
    print(f"🎯 URL: {url}")
    print("="*60 + "\n")
    
    try:
        with sync_playwright() as p:
            # Launch browser with anti-detection
            browser = p.chromium.launch(
                headless=False,  # Set to True for production
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--no-sandbox',
                    '--disable-dev-shm-usage'
                ]
            )
            
            # Create context with realistic settings
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
                extra_http_headers={
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'none',
                    'Upgrade-Insecure-Requests': '1',
                }
            )
            
            page = context.new_page()
            
            # Step 1: Apply Stealth Mode
            print("🕵️  Step 1: Applying stealth mode...")
            stealth_applied = CustomCaptchaBypass.apply_stealth_mode(page)
            if stealth_applied:
                print("✅ Stealth mode applied successfully\n")
            else:
                print("❌ Stealth mode failed\n")
            
            # Step 2: Navigate to page
            print(f"🌐 Step 2: Navigating to {url}...")
            try:
                response = page.goto(url, wait_until='domcontentloaded', timeout=30000)
                print(f"✅ Page loaded - Status: {response.status}\n")
            except Exception as nav_error:
                print(f"❌ Navigation error: {nav_error}\n")
                return False
            
            # Step 3: Check for Cloudflare
            print("🔍 Step 3: Checking for Cloudflare...")
            is_cloudflare = CustomCaptchaBypass.detect_cloudflare(page)
            
            if is_cloudflare:
                print("🛡️  Cloudflare challenge detected!")
                print("⏳ Attempting bypass (waiting for auto-complete)...")
                
                cloudflare_bypassed = CustomCaptchaBypass.bypass_cloudflare(page, timeout=30000)
                
                if cloudflare_bypassed:
                    print("✅ Cloudflare bypassed successfully!\n")
                else:
                    print("⚠️  Cloudflare bypass timeout - continuing anyway...\n")
            else:
                print("✅ No Cloudflare detected\n")
            
            # Step 4: Check for Captcha
            print("🔍 Step 4: Checking for captchas...")
            captcha_info = CustomCaptchaBypass.detect_captcha(page)
            
            if captcha_info['detected']:
                print(f"🔐 Captcha detected: {captcha_info['type']}")
                print("⏳ Attempting auto-solve...")
                
                captcha_solved = CustomCaptchaBypass.auto_solve_captcha(page, captcha_info, timeout=60000)
                
                if captcha_solved:
                    print("✅ Captcha bypassed successfully!\n")
                else:
                    print("⚠️  Captcha bypass failed - continuing anyway...\n")
            else:
                print("✅ No captcha detected\n")
            
            # Step 5: Wait for content
            print("⏳ Step 5: Waiting for page content...")
            try:
                page.wait_for_load_state('networkidle', timeout=10000)
                print("✅ Page fully loaded\n")
            except:
                print("⚠️  Timeout waiting for networkidle - continuing...\n")
            
            # Step 6: Check results
            print("📊 Step 6: Analyzing page content...")
            
            # Get page content
            content = page.content()
            current_url = page.url
            title = page.title()
            
            # Check if we're still on challenge page
            if 'cloudflare' in current_url.lower() or 'challenge' in current_url.lower():
                print("❌ Still on challenge page")
                print(f"   Current URL: {current_url}")
                return False
            
            # Check for property listings
            properties_found = False
            if 'property' in content.lower() and ('rent' in content.lower() or 'listing' in content.lower()):
                properties_found = True
            
            # Check for specific PropertyGuru elements
            property_cards = page.locator('[data-listing-id]').count()
            
            print(f"   Title: {title}")
            print(f"   Current URL: {current_url}")
            print(f"   Content Length: {len(content)} bytes")
            print(f"   Property Cards Found: {property_cards}")
            
            if property_cards > 0:
                print(f"\n✅ SUCCESS! Found {property_cards} property listings")
                
                # Get first few listings as proof
                print("\n📋 Sample Listings:")
                for i in range(min(3, property_cards)):
                    try:
                        listing = page.locator('[data-listing-id]').nth(i)
                        listing_id = listing.get_attribute('data-listing-id')
                        print(f"   • Listing ID: {listing_id}")
                    except:
                        pass
                
                return True
            elif properties_found:
                print("\n✅ SUCCESS! Page content retrieved (property data found)")
                return True
            else:
                print("\n⚠️  WARNING: Page loaded but no clear property listings found")
                print("   This might still be blocked or require more time")
                return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            browser.close()
        except:
            pass

if __name__ == "__main__":
    print("\n🚀 Starting PropertyGuru Bypass Test\n")
    
    success = test_propertyguru()
    
    print("\n" + "="*60)
    if success:
        print("✅ TEST PASSED - Bypass Working!")
    else:
        print("❌ TEST FAILED - Bypass Not Working")
    print("="*60 + "\n")
    
    sys.exit(0 if success else 1)
