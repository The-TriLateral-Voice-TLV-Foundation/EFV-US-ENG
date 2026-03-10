# TLV Emotional and Feeling Vocabulary (EFV)
## Auto-Index, TOC, and API System

Complete solution for indexing, maintaining, and serving your TLV EFV vocabulary via REST API, Word of the Day services, and RSS feeds.

---

## 📋 Overview

This system provides:

✅ **Auto-Indexing** - Automatically scans all `.json` files (a-z)  
✅ **Table of Contents** - Multi-level TOC by letter, category, and precision  
✅ **JSON Indices** - Searchable indices for programmatic access  
✅ **API Server** - REST endpoints for Word of Day, search, RSS feeds  
✅ **CSV Exports** - Multiple formats for Word of Day apps, RSS, spreadsheets  
✅ **Watch Mode** - Automatically regenerates indices when vocab updates  
✅ **Scalable** - Designed to grow as your vocabulary expands  

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the scripts
cd /path/to/your/EFV\ directory

# Install Python dependencies
pip install -r requirements.txt

# Or manually install
pip install watchdog flask flask-cors feedgen python-dateutil
```

### 2. Generate Indices (First Run)

```bash
# Generate all indices from your vocabulary files
python efv_index_generator.py

# Or specify custom paths
python efv_index_generator.py --base-dir ~/EFV\ US\ ENG --output-dir ~/EFV\ _indices
```

**Output files created in `_indices/` directory:**
- `00_TABLE_OF_CONTENTS.md` - Full TOC for documentation
- `01_INDEX.json` - Searchable JSON index
- `02_API_MANIFEST.json` - API endpoint documentation
- `03_VOCABULARY_FULL.csv` - Complete vocabulary export
- `04_WORD_OF_DAY.csv` - Format for daily word apps
- `05_RSS_FEED_DATA.csv` - Format for RSS feeds
- `MANIFEST.json` - File manifest and statistics

### 3. Start API Server

```bash
# Start the API server
python efv_api_server.py

# Or with custom settings
python efv_api_server.py --host 0.0.0.0 --port 5000 --debug
```

Server runs on `http://localhost:5000`

### 4. (Optional) Watch for Changes

```bash
# Automatically regenerate indices when vocab files change
python efv_index_generator.py --watch

# Keep this running in a terminal while editing vocabulary
```

---

## 📖 Usage Examples

### Generate Indices Only

```bash
python efv_index_generator.py
```

Creates all index files in `_indices/` directory.

### Watch Mode (Auto-Update)

```bash
# Terminal 1: Watch for changes
python efv_index_generator.py --watch

# Terminal 2: Edit your a.json, b.json, etc.
# Indices automatically regenerate when files change
```

### API Server

```bash
# Terminal: Start API
python efv_api_server.py

# In another terminal or browser:
curl http://localhost:5000/api/v1/metadata
curl http://localhost:5000/api/v1/word-of-day
curl http://localhost:5000/api/v1/word/random
curl "http://localhost:5000/api/v1/word/ABHORRED"
curl "http://localhost:5000/api/v1/search?q=disgust"
```

### CSV Export Formats

```bash
# Full export (all fields)
python efv_index_generator.py --export csv --format full

# Word of the Day format
python efv_index_generator.py --export csv --format wotd

# RSS feed format
python efv_index_generator.py --export csv --format rss
```

---

## 🔌 API Endpoints

All endpoints return JSON responses.

### Core Endpoints

#### Word of the Day
```
GET /api/v1/word-of-day
GET /api/v1/word-of-day?date=2025-12-27
```
**Returns:** Word + category + precision level for specific date

#### Random Word
```
GET /api/v1/word/random
```
**Returns:** Random word from vocabulary

#### Specific Word
```
GET /api/v1/word/{word}
```
**Returns:** Full word metadata including all 7 sections

#### Words by Category
```
GET /api/v1/category/{category}
GET /api/v1/category/Disgust
```
**Returns:** All words in category

#### Words by Letter
```
GET /api/v1/letter/{letter}
GET /api/v1/letter/A
```
**Returns:** All words starting with letter

#### Search
```
GET /api/v1/search?q={query}
GET /api/v1/search?q=despair
```
**Returns:** Matching words (name or category)

### Feed & Export Endpoints

#### RSS Feed
```
GET /rss/daily-word.xml
```
**Returns:** 30-day RSS feed of word-of-day entries

#### CSV Export
```
GET /export/csv
GET /export/csv?format=full
GET /export/csv?format=wotd
```
**Returns:** CSV in specified format

### Metadata Endpoints

#### API Metadata
```
GET /api/v1/metadata
```
**Returns:** API info, endpoints, categories, letters

#### Health Check
```
GET /health
```
**Returns:** Server status

---

## 📁 Directory Structure

```
EFV US ENG/
├── a.json
├── b.json
├── ... (c through z.json)
├── 1. TriLateral-Voice...md
├── efv_index_generator.py      ← Index generator script
├── efv_api_server.py           ← API server script
├── requirements.txt            ← Python dependencies
├── README.md                   ← This file
└── _indices/
    ├── 00_TABLE_OF_CONTENTS.md ← Generated TOC
    ├── 01_INDEX.json           ← Searchable index
    ├── 02_API_MANIFEST.json    ← API documentation
    ├── 03_VOCABULARY_FULL.csv  ← Full export
    ├── 04_WORD_OF_DAY.csv      ← Word of Day format
    ├── 05_RSS_FEED_DATA.csv    ← RSS format
    └── MANIFEST.json           ← File manifest
```

---

## 🔧 Configuration

### Specify Custom Paths

```bash
python efv_index_generator.py \
  --base-dir ~/my-vocab \
  --output-dir ~/my-vocab/_indices
```

### API Server Configuration

```bash
python efv_api_server.py \
  --index-dir ~/my-vocab/_indices \
  --host 127.0.0.1 \
  --port 8080 \
  --debug
```

### Watch Multiple Directories

Use `--base-dir` to point to your vocabulary directory:

```bash
python efv_index_generator.py --base-dir ~/EFV\ US\ ENG --watch
```

---

## 📊 Output Examples

### Table of Contents

Generated `00_TABLE_OF_CONTENTS.md` includes:

- **By Letter** - List of all words organized A-Z
- **By Category** - All 38 emotional categories with word counts
- **Statistics** - Total words, letters, categories, generation date
- **Quick navigation** - Links to each section

### JSON Index

Generated `01_INDEX.json` structure:

```json
{
  "metadata": {
    "title": "TLV Emotional and Feeling Vocabulary Index",
    "version": "1.0",
    "generated": "2025-12-27T...",
    "total_words": 2847,
    "letters": ["A", "B", ..., "Z"],
    "categories": ["Joy/Happiness", "Fear/Anxiety", ...]
  },
  "by_letter": {
    "A": [
      {
        "word": "ABHORRED",
        "letter": "A",
        "category": "Disgust/Aversion",
        "precision_level": "HIGH",
        ...
      }
    ]
  },
  "by_category": { ... },
  "all_words": [ ... ]
}
```

### CSV Formats

**Full Export (03_VOCABULARY_FULL.csv):**
```
word,letter,category,precision_level,somatic_integration,temporal_translation,cultural_bridge,file_path,last_updated
ABHORRED,A,Disgust/Aversion,HIGH,YES,NO,RECOMMENDED,/path/to/a.json,2025-12-27T...
...
```

**Word of Day (04_WORD_OF_DAY.csv):**
```
word,category,precision_level,etymology_summary
ABHORRED,Disgust/Aversion,HIGH,"- **Root Language**: Latin 'abhorrēre'..."
...
```

**RSS Feed (05_RSS_FEED_DATA.csv):**
```
word,category,etymology_summary,date
ABHORRED,Disgust/Aversion,"- **Root Language**: Latin 'abhorrēre'...",2025-12-27
...
```

---

## 🌐 Integration Examples

### Word of the Day App

Use the CSV export or API endpoint:

```python
import requests

# Get today's word
response = requests.get('http://localhost:5000/api/v1/word-of-day')
word_data = response.json()

print(f"Word: {word_data['word']}")
print(f"Category: {word_data['category']}")
print(f"Precision: {word_data['precision_level']}")
```

### Email Mailing List

Use the CSV export with your email service:

```bash
# Export CSV suitable for email
python efv_index_generator.py --export csv --format wotd

# Use 04_WORD_OF_DAY.csv with your email service
# (Mailchimp, SendGrid, etc.)
```

### RSS Reader

Subscribe to RSS feed:

```
http://localhost:5000/rss/daily-word.xml
```

Add to any RSS reader (Feedly, Apple News, etc.)

### Website Integration

```html
<!-- Embed Word of the Day in website -->
<div id="word-of-day"></div>

<script>
fetch('http://your-api.com/api/v1/word-of-day')
  .then(r => r.json())
  .then(data => {
    document.getElementById('word-of-day').innerHTML = `
      <h3>${data.word}</h3>
      <p>Category: ${data.category}</p>
      <p>Precision: ${data.precision_level}</p>
    `;
  });
</script>
```

---

## 🔄 Workflow

### Adding New Words

1. **Edit vocabulary files** (a.json, b.json, etc.)
2. **Save changes**
3. **Indices auto-regenerate** (if watching) OR
4. **Manually run** `python efv_index_generator.py`
5. **API automatically reflects** new words

### Updating Existing Words

1. **Edit word entry** in JSON file
2. **Save**
3. **Indices auto-update**
4. **API serves new version**

### Expanding Vocabulary

The system automatically handles:
- New word additions
- Category changes
- Precision level updates
- Somatic integration changes
- All other metadata updates

No additional configuration needed.

---

## 📈 Performance

- **Scanning Time**: ~2-5 seconds for 2,000+ words
- **Index Generation**: ~3-8 seconds
- **API Response Time**: <100ms for cached queries
- **Memory Usage**: ~50-100MB for typical EFV vocabulary

---

## 🐛 Troubleshooting

### "No JSON files found"

**Error:** `⚠️ No JSON files found in {directory}`

**Solution:**
```bash
# Make sure you're in correct directory
cd /path/to/EFV\ US\ ENG

# Verify .json files exist
ls *.json

# Run with explicit path
python efv_index_generator.py --base-dir ./
```

### "Index file not found" (API Error)

**Error:** When starting API server

**Solution:**
```bash
# Generate indices first
python efv_index_generator.py

# Then start API
python efv_api_server.py
```

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Use different port
python efv_api_server.py --port 8080

# Or kill existing process
lsof -ti:5000 | xargs kill -9
```

### Watch Mode Not Detecting Changes

**Solution:**
- Ensure file system supports file watchers (most do)
- On macOS/Linux: install watchdog with inotify support
- On Windows: ensure file saved to same directory

---

## 📝 requirements.txt

```
watchdog>=3.0.0
flask>=2.3.0
flask-cors>=4.0.0
feedgen>=1.1.0
python-dateutil>=2.8.2
```

---

## 🔐 Security

- API runs on localhost by default
- Use `--host 127.0.0.1` to restrict access
- Deploy behind a reverse proxy (nginx, Apache) for production
- Add authentication/rate limiting for public deployment

---

## 📜 License

This tool is part of the TLV Framework.

Licensed under: **CC BY-NC-SA 4.0**
- Non-commercial use: Free
- Commercial use: Requires license
- Contact: licensing@tlvfoundation.org

---

## 📞 Support

For issues or questions:
- Check troubleshooting section above
- Review script documentation
- Verify JSON file structure matches a.json format
- Ensure all vocabulary files valid JSON

---

## 🎯 Next Steps

1. ✅ **Generate indices**: `python efv_index_generator.py`
2. ✅ **Start API**: `python efv_api_server.py`
3. ✅ **Test endpoints**: Visit `http://localhost:5000/api/v1/metadata`
4. ✅ **Setup Word of Day**: Use CSV or API endpoint
5. ✅ **Configure RSS**: Subscribe to `/rss/daily-word.xml`
6. ✅ **Enable watch mode**: `python efv_index_generator.py --watch`

---

**Version:** 1.0  
**Last Updated:** December 27, 2025  
**Author:** TLV Development Team  
© 2025 The TriLateral Voice Foundation
