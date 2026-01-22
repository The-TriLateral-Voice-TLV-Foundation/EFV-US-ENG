#!/usr/bin/env bash

set -euo pipefail

# TLV EFV Index & API System - Quick Setup Script
# Generates indices, sets up API, and provides quick-start commands

set -e

echo "======================================================================"
echo " TriLateral Voice (TLV) Emotional and Feeling Vocabulary (EFV)"
echo " Auto-Index, TOC, and API System Setup"
echo "======================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check Python installation
echo -e "${BLUE}📋 Checking Python installation...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found. Please install Python 3.8+${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"
echo ""

# Check for pip
echo -e "${BLUE}📦 Checking pip installation...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 not found${NC}"
    exit 1
fi

echo -e "${GREEN}✓ pip3 found${NC}"
echo ""

# Install dependencies
echo -e "${BLUE}📥 Installing dependencies...${NC}"
if [ -f "requirements.txt" ]; then
    pip3 install -r requirements.txt
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️ requirements.txt not found. Installing manually...${NC}"
    pip3 install watchdog flask flask-cors feedgen python-dateutil
    echo -e "${GREEN}✓ Dependencies installed${NC}"
fi

echo ""

# Resolve to directory of this script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Use repo root (adjust if setup.sh lives in a subdir)
REPO_ROOT="${SCRIPT_DIR}"

# Generate indices
echo -e "${BLUE}Generating indices...${NC}"
python3 efv_index_generator.py

OUT_DIR="${REPO_ROOT}/vocab/_indices"

# Check if indices were created (use absolute path)
if [ -f "${OUT_DIR}/00_TABLE_OF_CONTENTS.md" ]; then
    echo -e "${GREEN}✓ Indices generated successfully!${NC}"
    echo ""
    
    echo -e "${BLUE}Summary${NC}"
    if [ -f "${OUT_DIR}/MANIFEST.json" ]; then
        python3 << PYEOF
import json
m = json.load(open("${OUT_DIR}/MANIFEST.json", "r", encoding="utf-8"))
s = m["statistics"]
print(f"Total words: {s['total_words']}")
print(f"Total letters: {s['total_letters']}")
print(f"Total categories: {s['total_categories']}")
PYEOF

    fi
else
    echo -e "${RED}❌ Index generation failed!${NC}"
    echo "Expected file not found: ${OUT_DIR}/00_TABLE_OF_CONTENTS.md"
    exit 1
fi

echo ""
echo -e "${BLUE}=====================================================================${NC}"
echo -e "${GREEN}🎉 Setup complete!${NC}"
echo -e "${BLUE}=====================================================================${NC}"
echo ""

echo -e "${YELLOW}📖 Generated Files:${NC}"
echo " • vocab/_indices/00_TABLE_OF_CONTENTS.md (Documentation TOC)"
echo " • vocab/_indices/01_INDEX.json (Searchable index)"
echo " • vocab/_indices/02_API_MANIFEST.json (API documentation)"
echo " • vocab/_indices/03_VOCABULARY_FULL.csv (Full export)"
echo " • vocab/_indices/04_WORD_OF_DAY.csv (Word of Day format)"
echo " • vocab/_indices/05_RSS_FEED_DATA.csv (RSS format)"
echo " • vocab/_indices/MANIFEST.json (File manifest)"
echo ""

echo -e "${YELLOW}🚀 Next Steps:${NC}"
echo ""

echo "1. Start the API server:"
echo -e " ${BLUE}python3 efv_api_server.py${NC}"
echo ""

echo "2. In another terminal, test endpoints:"
echo -e " ${BLUE}curl http://localhost:5000/api/v1/word-of-day${NC}"
echo -e " ${BLUE}curl http://localhost:5000/api/v1/word/random${NC}"
echo -e " ${BLUE}curl http://localhost:5000/api/v1/metadata${NC}"
echo ""

echo "3. Auto-regenerate indices when vocabulary changes:"
echo -e " ${BLUE}python3 efv_index_generator.py --watch${NC}"
echo ""

echo -e "${YELLOW}📚 Documentation:${NC}"
echo " • Full guide: See README_EFV_SYSTEM.md"
echo " • TOC: vocab/_indices/00_TABLE_OF_CONTENTS.md"
echo " • API: http://localhost:5000/api/v1/metadata (when server running)"
echo ""

echo -e "${YELLOW}💡 Common Commands:${NC}"
echo " # Generate indices"
echo -e " ${BLUE}python3 efv_index_generator.py${NC}"
echo ""

echo " # Watch for changes (auto-regenerate)"
echo -e " ${BLUE}python3 efv_index_generator.py --watch${NC}"
echo ""

echo " # Start API server"
echo -e " ${BLUE}python3 efv_api_server.py${NC}"
echo ""

echo " # Export specific format"
echo -e " ${BLUE}python3 efv_index_generator.py --export csv --format wotd${NC}"
echo ""

echo -e "${BLUE}=====================================================================${NC}"
echo -e "${GREEN}Happy indexing! 🎯${NC}"
echo -e "${BLUE}=====================================================================${NC}"