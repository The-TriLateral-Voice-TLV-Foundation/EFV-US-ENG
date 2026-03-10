#!/usr/bin/env bash
# TLV-EFV Setup Script
# ====================
# Sets up the data directory structure and launches the API.
#
# Usage:
#   chmod +x setup.sh && ./setup.sh
#
# Prerequisites: Python 3.9+, pip

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "╔══════════════════════════════════════════════════╗"
echo "║   TLV Emotional & Feeling Vocabulary — Setup    ║"
echo "╚══════════════════════════════════════════════════╝"

# 1. Create directory structure
echo "→ Creating directory structure…"
mkdir -p data/entries/{a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z}
mkdir -p data/indices
mkdir -p frontend

# 2. Copy/move data files if not in place
if [ -f "efv-a.json" ] && [ ! -f "data/efv-a.json" ]; then
    echo "→ Moving letter bundle files into data/…"
    mv efv-*.json data/ 2>/dev/null || true
fi

if [ -f "master_index.json" ] && [ ! -f "data/indices/master_index.json" ]; then
    echo "→ Moving index files…"
    mv master_index.json data/indices/ 2>/dev/null || true
    mv intensity.json data/indices/ 2>/dev/null || true
    mv somatic_region.json data/indices/ 2>/dev/null || true
fi

# Move individual entry files
if [ -d "entries" ] && [ ! -f "data/entries/a/abhorred.json" ]; then
    echo "→ Moving individual entry files…"
    cp -r entries/* data/entries/ 2>/dev/null || true
fi

# Copy frontend
if [ -f "index.html" ] && [ ! -f "frontend/index.html" ]; then
    cp index.html frontend/
fi

# 3. Install dependencies
echo "→ Installing Python dependencies…"
pip install fastapi uvicorn aiofiles python-multipart 2>/dev/null || pip3 install fastapi uvicorn aiofiles python-multipart

# 4. Launch
echo ""
echo "✅ Setup complete!"
echo ""
echo "→ Starting API server…"
echo "  API:      http://localhost:8000/api/stats"
echo "  Frontend: http://localhost:8000"
echo "  Docs:     http://localhost:8000/docs"
echo ""
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
