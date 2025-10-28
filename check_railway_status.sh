#!/bin/bash

echo "================================================"
echo "Checking Railway Deployment Status"
echo "================================================"
echo ""

# Check health endpoint
echo "📊 Checking backend health..."
HEALTH=$(curl -s "https://database-ingestion-production.up.railway.app/health")
echo "$HEALTH" | python3 -m json.tool 2>/dev/null || echo "$HEALTH"
echo ""

# Test with verbose logging
echo "================================================"
echo "🧪 Testing PropertyGuru with detailed output"
echo "================================================"
echo ""

curl -X POST "https://database-ingestion-production.up.railway.app/api/ingest-url" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://www.propertyguru.com.sg/property-for-rent",
    "project": "test-crawl",
    "index_name": "document-knowledge-base",
    "max_pages": 1,
    "max_depth": 0
  }' \
  -w "\n\nHTTP Status: %{http_code}\nTime: %{time_total}s\n" \
  --max-time 120 2>&1 | tee /tmp/railway_test.log

echo ""
echo "================================================"
echo "📋 Analysis"
echo "================================================"

if grep -q "success.*true" /tmp/railway_test.log; then
    echo "✅ SUCCESS! PropertyGuru crawling works!"
elif grep -q "No crawlable pages" /tmp/railway_test.log; then
    echo "❌ FAILED: All fetch methods blocked"
    echo ""
    echo "This means:"
    echo "  1. Railway deployment may not be complete yet"
    echo "  2. OR Chromium not installed properly"
    echo "  3. OR PropertyGuru blocking Railway's IP"
    echo ""
    echo "Next steps:"
    echo "  → Check Railway logs for 'playwright install chromium'"
    echo "  → Look for 'Downloading Chromium...' in build logs"
    echo "  → Check for 'fetch_with_playwright succeeded' in runtime logs"
elif grep -q "timeout" /tmp/railway_test.log; then
    echo "⏱️  TIMEOUT: Backend is working on it (slow)"
    echo "This might mean Playwright is trying but taking long"
fi

echo ""
echo "================================================"
echo "🔗 Important Links"
echo "================================================"
echo ""
echo "Railway Dashboard: https://railway.app/dashboard"
echo "Check Logs: Click on backend service → Logs tab"
echo ""
echo "What to look for in Railway logs:"
echo "  ✓ 'Downloading Chromium...'"
echo "  ✓ 'Chromium installed successfully'"
echo "  ✓ 'Attempting to fetch: https://www.propertyguru...'"
echo "  ✓ 'fetch_with_playwright succeeded'"
echo ""
