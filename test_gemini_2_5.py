"""
Test Gemini 2.5 Flash Live Model
"""

import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment
load_dotenv('backend/.env')

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in backend/.env")
    sys.exit(1)

print("🔑 API Key found")
print(f"🔑 Key: {GEMINI_API_KEY[:10]}...")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

print("\n" + "="*60)
print("Testing Gemini Models")
print("="*60 + "\n")

# Test models
models_to_test = [
    'models/gemini-2.5-flash-live',
    'models/gemini-2.0-flash-live',
    'models/gemini-2.0-flash-exp',
    'models/gemini-1.5-flash'
]

for model_name in models_to_test:
    print(f"📡 Testing: {model_name}")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello' in one word")
        
        # Get the text
        result_text = response.text.strip()
        
        print(f"   ✅ SUCCESS: {model_name}")
        print(f"   Response: {result_text[:50]}")
        print()
        
    except Exception as e:
        error_msg = str(e)
        if '404' in error_msg or 'not found' in error_msg.lower():
            print(f"   ❌ NOT AVAILABLE: {model_name}")
            print(f"   Error: Model not found (404)")
        elif 'quota' in error_msg.lower() or 'limit' in error_msg.lower():
            print(f"   ⚠️  QUOTA/LIMIT: {model_name}")
            print(f"   Error: {error_msg[:100]}")
        else:
            print(f"   ❌ ERROR: {model_name}")
            print(f"   Error: {error_msg[:100]}")
        print()

print("="*60)
print("✅ Test Complete")
print("="*60)
