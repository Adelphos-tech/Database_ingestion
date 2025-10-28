#!/usr/bin/env python3
"""
Test script to verify PropertyGuru crawling with bypass mechanisms
"""
import requests
import json
import sys

# Test URLs
TEST_URL = "https://www.propertyguru.com.sg/property-for-rent"
API_URL = "https://database-ingestion-production.up.railway.app/api/ingest-url"

def test_crawl():
    print("🔍 Testing PropertyGuru Crawl with Bypass Mechanisms")
    print(f"Target URL: {TEST_URL}")
    print(f"API Endpoint: {API_URL}\n")
    
    payload = {
        "url": TEST_URL,
        "project": "test-crawl",
        "index_name": "document-knowledge-base",
        "max_pages": 1,  # Just test 1 page first
        "max_depth": 0   # Only the main page
    }
    
    print("📤 Sending request to backend...")
    print(f"Payload: {json.dumps(payload, indent=2)}\n")
    
    try:
        response = requests.post(
            API_URL,
            json=payload,
            timeout=60,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        try:
            data = response.json()
            print(f"\n📄 Response Body:")
            print(json.dumps(data, indent=2))
            
            if response.status_code == 200 and data.get('success'):
                print("\n✅ SUCCESS! Crawling works!")
                print(f"✅ Pages ingested: {len(data.get('ingested', []))}")
                print(f"✅ Total chunks: {data.get('total_chunks', 0)}")
                if data.get('ingested'):
                    for page in data['ingested']:
                        print(f"  - {page.get('title', 'Untitled')} ({page.get('chunks', 0)} chunks)")
                return True
            else:
                print("\n❌ FAILED!")
                error = data.get('error', 'Unknown error')
                print(f"❌ Error: {error}")
                
                if 'No crawlable pages' in error:
                    print("\n🔍 Diagnosis:")
                    print("  - All 3 fetch methods failed (requests, cloudscraper, playwright)")
                    print("  - Possible causes:")
                    print("    1. ENABLE_PLAYWRIGHT_CRAWL is not set to 'true' in .env")
                    print("    2. Playwright is not installed (pip install playwright)")
                    print("    3. Playwright browsers not installed (playwright install chromium)")
                    print("    4. Website has very strong bot protection")
                    print("\n📝 Recommended actions:")
                    print("  1. Check Railway/deployment logs for fetch method results")
                    print("  2. Set ENABLE_PLAYWRIGHT_CRAWL=true in environment")
                    print("  3. Consider adding proxy if IP is blocked")
                return False
                
        except json.JSONDecodeError:
            print(f"\n❌ Invalid JSON response")
            print(f"Raw response: {response.text[:500]}")
            return False
            
    except requests.Timeout:
        print("❌ Request timeout (60s)")
        print("The backend is taking too long. This might mean:")
        print("  - Playwright is trying but website is slow")
        print("  - All methods are being tried sequentially")
        return False
    except requests.RequestException as e:
        print(f"❌ Request failed: {e}")
        return False

def test_simple_site():
    """Test with a simple site first to verify endpoint works"""
    print("\n" + "="*60)
    print("🧪 Testing with simple site first (example.com)")
    print("="*60 + "\n")
    
    payload = {
        "url": "https://example.com",
        "project": "test-simple",
        "index_name": "document-knowledge-base",
        "max_pages": 1,
        "max_depth": 0
    }
    
    try:
        response = requests.post(API_URL, json=payload, timeout=30)
        print(f"📊 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Simple site works! Endpoint is functioning.")
                return True
        print("⚠️ Even simple site failed - endpoint may be broken")
        print(f"Response: {response.text[:200]}")
        return False
    except Exception as e:
        print(f"❌ Failed: {e}")
        return False

if __name__ == "__main__":
    print("="*60)
    print("PropertyGuru Crawl Test Suite")
    print("="*60 + "\n")
    
    # Test 1: Simple site
    simple_works = test_simple_site()
    
    if not simple_works:
        print("\n❌ Cannot proceed - basic endpoint not working")
        sys.exit(1)
    
    # Test 2: PropertyGuru
    print("\n" + "="*60)
    print("🏠 Testing PropertyGuru (Protected Site)")
    print("="*60 + "\n")
    
    success = test_crawl()
    
    if success:
        print("\n🎉 All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ PropertyGuru test failed")
        print("\n💡 Next steps:")
        print("  1. Check if ENABLE_PLAYWRIGHT_CRAWL=true in Railway environment")
        print("  2. Review Railway deployment logs")
        print("  3. Verify playwright and dependencies are installed")
        sys.exit(1)
