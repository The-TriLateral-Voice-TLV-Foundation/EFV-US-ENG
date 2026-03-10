# TLV EFV System - Quick Reference Guide

Fast lookup for common tasks and API usage.

---

## ⚡ Quick Commands

### First-Time Setup
```bash
chmod +x setup.sh
./setup.sh
```

### Generate Indices
```bash
python3 efv_index_generator.py
```

### Watch for Changes
```bash
python3 efv_index_generator.py --watch
```

### Start API Server
```bash
python3 efv_api_server.py
```

### Custom Paths
```bash
python3 efv_index_generator.py \
  --base-dir ~/my-vocab \
  --output-dir ~/my-vocab/_indices
```

---

## 🔌 API Quick Reference

All URLs: `http://localhost:5000`

### Get Word of the Day
```bash
curl http://localhost:5000/api/v1/word-of-day
curl http://localhost:5000/api/v1/word-of-day?date=2025-12-25
```

### Get Random Word
```bash
curl http://localhost:5000/api/v1/word/random
```

### Get Specific Word
```bash
curl http://localhost:5000/api/v1/word/ABHORRED
curl http://localhost:5000/api/v1/word/ACCEPTED
```

### Search
```bash
curl "http://localhost:5000/api/v1/search?q=disgust"
curl "http://localhost:5000/api/v1/search?q=fear"
```

### Browse by Category
```bash
curl http://localhost:5000/api/v1/category/Disgust
curl "http://localhost:5000/api/v1/category/Sadness/Grief"
```

### Browse by Letter
```bash
curl http://localhost:5000/api/v1/letter/A
curl http://localhost:5000/api/v1/letter/Z
```

### Get API Info
```bash
curl http://localhost:5000/api/v1/metadata
curl http://localhost:5000/health
```

### RSS Feed
```bash
http://localhost:5000/rss/daily-word.xml
```

### CSV Export
```bash
curl http://localhost:5000/export/csv > full.csv
curl "http://localhost:5000/export/csv?format=wotd" > wotd.csv
curl "http://localhost:5000/export/csv?format=rss" > rss.csv
```

---

## 💻 Python Integration Examples

### Get Word of the Day
```python
import requests

response = requests.get('http://localhost:5000/api/v1/word-of-day')
data = response.json()

print(data['word'])              # ABHORRED
print(data['category'])          # Disgust/Aversion
print(data['precision_level'])   # HIGH
print(data['date'])              # 2025-12-27
```

### Get Random Word
```python
import requests

response = requests.get('http://localhost:5000/api/v1/word/random')
word = response.json()

print(f"{word['word']}: {word['category']}")
```

### Search Vocabulary
```python
import requests

response = requests.get(
    'http://localhost:5000/api/v1/search',
    params={'q': 'fear'}
)
results = response.json()['results']

for result in results:
    print(f"{result['word']} - {result['category']}")
```

### Get Words in Category
```python
import requests

response = requests.get(
    'http://localhost:5000/api/v1/category/Disgust'
)
data = response.json()

print(f"Category: {data['category']}")
print(f"Words: {data['word_count']}")

for word in data['words']:
    print(f"  • {word['word']}")
```

### List All Words by Letter
```python
import requests

response = requests.get('http://localhost:5000/api/v1/letter/A')
data = response.json()

print(f"Letter {data['letter']}: {data['word_count']} words")
for word in data['words']:
    print(f"  • {word['word']}")
```

---

## 📊 CSV Export Formats

### Full Format (03_VOCABULARY_FULL.csv)
Columns: word, letter, category, precision_level, somatic_integration, temporal_translation, cultural_bridge, file_path, last_updated

```csv
ABHORRED,A,Disgust/Aversion,HIGH,YES,NO,RECOMMENDED,...
```

### Word of Day Format (04_WORD_OF_DAY.csv)
Columns: word, category, precision_level, etymology_summary

```csv
ABHORRED,Disgust/Aversion,HIGH,"- **Root Language**: Latin 'abhorrēre'..."
```

### RSS Format (05_RSS_FEED_DATA.csv)
Columns: word, category, etymology_summary, date

```csv
ABHORRED,Disgust/Aversion,"- **Root Language**: Latin 'abhorrēre'...",2025-12-27
```

---

## 📁 Index File Structure

### 00_TABLE_OF_CONTENTS.md
Human-readable TOC with:
- Words organized by letter (A-Z)
- Words organized by category
- Statistics and generation info

### 01_INDEX.json
Machine-readable index with:
- `metadata` - API info
- `by_letter` - Words indexed by letter
- `by_category` - Words indexed by category
- `by_precision` - Words indexed by precision level
- `all_words` - Flat list of all words

### 02_API_MANIFEST.json
API endpoint documentation:
- Endpoint list
- Response format specification
- Available filters and parameters

### 03-05_*.csv
CSV exports in various formats for tools and services

### MANIFEST.json
File inventory and statistics:
- Generation timestamp
- File paths
- Word/category/letter counts

---

## 🔄 Workflow Examples

### Word of the Day App

**Initial Setup:**
```bash
python3 efv_index_generator.py
python3 efv_api_server.py
```

**In your app:**
```python
import requests
from datetime import date

daily_word = requests.get(
    'http://localhost:5000/api/v1/word-of-day'
).json()

display(daily_word['word'], daily_word['category'])
```

### Email Newsletter

**Option 1: Using CSV**
```bash
# Export to CSV
curl http://localhost:5000/export/csv?format=wotd > words.csv

# Upload to Mailchimp, SendGrid, etc.
```

**Option 2: Using API**
```python
import requests
from datetime import date, timedelta

# Send last 30 days of words
for i in range(30):
    target_date = date.today() - timedelta(days=i)
    word_data = requests.get(
        'http://localhost:5000/api/v1/word-of-day',
        params={'date': target_date.isoformat()}
    ).json()
    
    send_email(word_data)
```

### Website Widget

**HTML:**
```html
<div id="efv-wotd"></div>

<script>
fetch('http://api.example.com/api/v1/word-of-day')
  .then(r => r.json())
  .then(d => document.getElementById('efv-wotd').innerHTML = `
    <div class="word-of-day">
      <h3>${d.word}</h3>
      <p class="category">${d.category}</p>
      <p class="date">${d.date}</p>
    </div>
  `);
</script>
```

### RSS Feed Reader

**Subscribe in any RSS reader:**
- Feedly: Add feed `http://api.example.com/rss/daily-word.xml`
- Apple News: Add custom feed
- Google News: Add custom feed

---

## 📈 Performance Tips

### Cache API Responses
```python
import functools
import time

@functools.lru_cache(maxsize=128)
def get_word(word_name):
    # Result cached for 1 hour
    return fetch_api(word_name)
```

### Batch Operations
```python
# Instead of individual requests
metadata = requests.get('http://localhost:5000/api/v1/metadata').json()

# Then access local copies
words_by_category = metadata['categories']
```

### Index Local Copy
```python
import json

# Load index once at startup
with open('_indices/01_INDEX.json') as f:
    index = json.load(f)

# Use local index for fast queries
def find_word(name):
    for word in index['all_words']:
        if word['word'] == name:
            return word
```

---

## 🔒 Security Considerations

### For Production Deployment

1. **Restrict Access:**
   ```bash
   python3 efv_api_server.py --host 127.0.0.1 --port 5000
   ```

2. **Use Reverse Proxy (nginx):**
   ```nginx
   server {
       listen 80;
       server_name api.example.com;
       
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
       }
   }
   ```

3. **Add Authentication:**
   ```python
   # Modify efv_api_server.py to add API key requirement
   @app.before_request
   def check_auth():
       if request.args.get('key') != 'your-api-key':
           return {'error': 'Unauthorized'}, 401
   ```

4. **Rate Limiting:**
   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)
   
   @app.route('/api/v1/word-of-day')
   @limiter.limit("100 per hour")
   def word_of_day():
       ...
   ```

---

## 🐛 Debugging Tips

### Check Index Status
```bash
# View TOC
cat _indices/00_TABLE_OF_CONTENTS.md

# View manifest
cat _indices/MANIFEST.json

# Count words
python3 -c "import json; print(len(json.load(open('_indices/01_INDEX.json'))['all_words']))"
```

### Test API Endpoints
```bash
# Basic connectivity
curl http://localhost:5000/health

# API metadata
curl http://localhost:5000/api/v1/metadata | python3 -m json.tool

# Specific word
curl http://localhost:5000/api/v1/word/TEST_WORD | python3 -m json.tool
```

### Check File Permissions
```bash
# Ensure scripts are executable
chmod +x *.py *.sh

# Ensure read access to vocab files
ls -l *.json

# Ensure write access to output directory
ls -ld _indices/
```

---

## 📚 Common Integration Patterns

### Pattern 1: Daily Rotation
```python
def get_word_for_day(day_num):
    """Deterministic: same word each day"""
    words = fetch_all_words()
    return words[day_num % len(words)]
```

### Pattern 2: Weekly Focus
```python
def get_weekly_category(week_num):
    """Rotate through categories weekly"""
    categories = fetch_categories()
    return categories[week_num % len(categories)]
```

### Pattern 3: Random but Tracked
```python
def get_random_word_with_tracking():
    """Random selection with duplicate prevention"""
    used = load_used_words()
    available = [w for w in all_words if w not in used]
    
    if not available:
        available = all_words
        clear_used_words()
    
    selected = random.choice(available)
    mark_used(selected)
    return selected
```

---

## 📞 Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "Port already in use" | Use `--port 8080` or kill existing process |
| "Index not found" | Run `python3 efv_index_generator.py` first |
| "No JSON files" | Ensure `*.json` files in current directory |
| "Permission denied" | Run `chmod +x *.sh` and `chmod +x *.py` |
| "Module not found" | Run `pip3 install -r requirements.txt` |
| "Watch not working" | Try manual regeneration, check file system |

---

## 📖 File Reference

| File | Purpose |
|------|---------|
| `efv_index_generator.py` | Generate all indices |
| `efv_api_server.py` | REST API server |
| `setup.sh` | Automated setup script |
| `requirements.txt` | Python dependencies |
| `README_EFV_SYSTEM.md` | Full documentation |
| `QUICK_REFERENCE.md` | This file |

---

**Last Updated:** December 27, 2025  
**Version:** 1.0
