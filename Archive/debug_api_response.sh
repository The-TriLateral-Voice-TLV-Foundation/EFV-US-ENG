# Quick test to see what your API actually returns

echo "Testing local API response..."
curl -s http://127.0.0.1:5000/api/v1/word-of-day | python3 -m json.tool

echo -e "\n\nTesting metadata endpoint..."
curl -s http://127.0.0.1:5000/api/v1/metadata | python3 -m json.tool
