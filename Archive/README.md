# TriLateral Voice (TLV)'s Emotional and Feeling Vocabulary API

**REST API for TLV Emotional and Feeling Vocabulary (RC0001)**

[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Version](https://img.shields.io/badge/version-RC0001-blue.svg)](https://tlvfoundation.org)
[![API Status](https://img.shields.io/badge/status-production--ready-green.svg)](https://github.com/your-repo)

---

## What is the EFV API?

The **Emotional and Feeling Vocabulary (EFV) API** provides programmatic access to the comprehensive emotional and somatic vocabulary that powers the **TriLateral Voice (TLV)** communication framework. 

Rather than limiting emotional language to a handful of basic terms, the EFV API delivers precision, cultural sensitivity, and embodied understanding of the full spectrum of human emotional experience—accessible through a simple, RESTful interface.

### Key Features

- **38 Emotional Categories** covering the full spectrum of human feeling
- **Word of the Day** endpoint for daily emotional vocabulary discovery
- **Six-Dimensional Documentation** for each emotion: etymology, contemporary usage, precise intent, conceptual explanation, cultural translation, and TLV application
- **Somatic Signature Mapping** linking emotions to physical sensations
- **Intensity Calibration (1–10)** for precise emotional depth across contexts
- **CSV and RSS Exports** for integration and distribution
- **Full-Text Search** for discovering emotions by concept or keyword
- **CORS-Enabled** for browser-based integration
- **Production-Ready** with health checks and metadata endpoints

---

## Quick Start

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd efv-api

# Install dependencies
pip install -r requirements.txt

# Generate indices (first time only)
python3 efv_index_generator.py

# Run the API server
python3 efv_api_server.py
```

The API will start on `http://localhost:5000`

### Try the API

```bash
# Word of the Day
curl http://localhost:5000/api/v1/word-of-day

# Random emotion word
curl http://localhost:5000/api/v1/word/random

# Specific word details
curl http://localhost:5000/api/v1/word/ABHORRED

# Words by category
curl http://localhost:5000/api/v1/category/Disgust

# Words by letter
curl http://localhost:5000/api/v1/letter/A

# Search
curl "http://localhost:5000/api/v1/search?q=fear"

# RSS feed (daily words)
curl http://localhost:5000/rss/daily-word.xml

# CSV export
curl http://localhost:5000/export/csv?format=full

# API metadata
curl http://localhost:5000/api/v1/metadata

# Health check
curl http://localhost:5000/health
```

---

## API Endpoints

### Core Endpoints

#### `GET /api/v1/word-of-day`
Returns a deterministically selected "Word of the Day" based on the current date. The same word is served to all users on the same day.

**Query Parameters:**
- `date` (optional) - ISO date string (e.g., `2025-01-22`) to get word for specific date

**Response:**
```json
{
  "status": "success",
  "date": "2025-01-22",
  "total_words": 2847,
  "word": "ABHORRED",
  "category": "Disgust",
  "precision_level": 9,
  "somatic_integration": "Full-body rejection response",
  "temporal_translation": "Consistently strong across eras",
  "cultural_bridge": "Universal human response to perceived violation",
  "sections": {
    "1": "Etymology & Historical Development",
    "2": "Contemporary Common Usage",
    "3": "Precise Evocation Intent",
    "4": "Conceptual Explanation",
    "5": "Cultural Translation Contexts",
    "6": "TLV Protocol Application",
    "7": "Somatic Signature Documentation"
  }
}
```

#### `GET /api/v1/word/random`
Returns a randomly selected word from the vocabulary.

**Response:**
```json
{
  "status": "success",
  "word": "JOYFUL",
  "category": "Joy/Happiness",
  "precision_level": 7
}
```

#### `GET /api/v1/word/<word_name>`
Returns complete documentation for a specific word.

**Parameters:**
- `word_name` - Word to retrieve (case-insensitive)

**Response:** Full 6-dimensional documentation including etymology, somatic signatures, cultural bridges, and TLV applications.

#### `GET /api/v1/category/<category_name>`
Returns all words in a specified emotional category.

**Parameters:**
- `category_name` - Category name (case-insensitive substring match)

**Response:**
```json
{
  "status": "success",
  "category": "Disgust",
  "word_count": 45,
  "words": [
    {"word": "ABHORRED", "precision_level": 9},
    {"word": "AVERSION", "precision_level": 8},
    ...
  ]
}
```

#### `GET /api/v1/letter/<letter>`
Returns all words starting with a specific letter.

**Parameters:**
- `letter` - Single letter (A-Z)

**Response:**
```json
{
  "status": "success",
  "letter": "A",
  "word_count": 89,
  "words": [
    {"word": "ABHORRED"},
    {"word": "ACCEPTANCE"},
    ...
  ]
}
```

#### `GET /api/v1/search`
Full-text search across word names and categories.

**Query Parameters:**
- `q` (required) - Query string (minimum 2 characters)

**Response:**
```json
{
  "status": "success",
  "query": "fear",
  "result_count": 28,
  "results": [
    {"word": "FEAR", "category": "Fear/Anxiety"},
    {"word": "FEARFUL", "category": "Fear/Anxiety"},
    ...
  ]
}
```

#### `GET /api/v1/metadata`
Returns API metadata including vocabulary statistics and available endpoints.

**Response:**
```json
{
  "status": "success",
  "api_version": "1.0",
  "total_words": 2847,
  "categories": ["Joy/Happiness", "Love/Affection", "Anger/Rage", ...],
  "letters": ["A", "B", "C", ...],
  "endpoints": {
    "word_of_day": "/api/v1/word-of-day",
    "random_word": "/api/v1/word/random",
    ...
  }
}
```

### Export Endpoints

#### `GET /rss/daily-word.xml`
Returns an RSS feed of the last 30 days of Words of the Day.

**Use Cases:**
- Subscribe to daily vocabulary in your RSS reader
- Integrate into email newsletters
- Syndicate to other platforms

#### `GET /export/csv`
Exports vocabulary data as CSV for analysis, import, or distribution.

**Query Parameters:**
- `format` - Export format:
  - `full` (default) - Complete vocabulary with all dimensions
  - `wotd` - Word of the Day format (word, category, precision_level)
  - `simple` - Minimal format (word, category)

**Response:** CSV file download with appropriate MIME type

### System Endpoints

#### `GET /health`
Health check endpoint for monitoring and deployment verification.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-01-22T20:07:15.123456+00:00",
  "words_loaded": 2847
}
```

---

## Directory Structure

```
efv-api/
├── efv_api_server.py          # Main Flask API server
├── efv_index_generator.py     # Generates searchable indices
├── requirements.txt            # Python dependencies
├── setup.sh                    # Deployment setup script
├── favicon.ico                 # API branding
├── README.md                   # This file
├── LICENSE                     # CC BY-NC-SA 4.0
└── vocab/
    ├── _indices/
    │   ├── 01_INDEX.json           # Master index (all words)
    │   ├── 02_API_MANIFEST.json    # Complete API documentation
    │   ├── 03_VOCABULARY_FULL.csv  # Full vocabulary export
    │   ├── 04_WORD_OF_DAY.csv      # Historical words of the day
    │   ├── 05_RSS_FEED_DATA.csv    # RSS feed data
    │   ├── CATEGORY_MAPPING.csv    # Category to words mapping
    │   ├── 00_TABLE_OF_CONTENTS.md # Index documentation
    │   └── MANIFEST.json           # Index metadata
    └── a.json - z.json             # Letter-indexed vocabulary (A-Z)
```

---

## Vocabulary Structure

Each emotion word in the EFV includes six dimensions of documentation:

### 1. Etymology & Historical Development
Root language, original meaning, semantic evolution, cultural shifts

### 2. Contemporary Common Usage
Primary definitions, colloquial usage, intensity calibration, temporal vulnerability

### 3. Precise Evocation Intent
Speaker experience, listener response, somatic markers, authenticity indicators

### 4. Conceptual Explanation
Core concept, phenomenology, relational context, temporal aspects

### 5. Cultural Translation Contexts
Framework perspectives (Western, Eastern, Indigenous, Clinical, Spiritual), cross-cultural variations, bridge examples

### 6. TLV Protocol Application
Usage in Speaker's Voice, Emotional/Somatic Voice, Observer's Voice, precision requirements

### Somatic Signature Documentation
- **Physical location mapping**: Body regions and sensation patterns
- **Kinesthetic response patterns**: Posture, gesture, breathing, movement
- **Neurobiological correlates**: Brain activation, chemical signatures
- **Intensity mapping (1–10)**: Subtle to peak experience
- **Resonance practices**: Emotional regulation and grounding
- **Cultural somatic variations**: Universal and culture-specific patterns

---

## Emotional Categories (38 Total)

Joy/Happiness, Love/Affection, Anger/Rage, Sadness/Grief, Fear/Anxiety, Surprise/Wonder, Disgust/Aversion, Shame/Guilt, Pride/Confidence, Envy/Jealousy, Contempt/Disdain, Curiosity/Interest, Boredom/Apathy, Hope/Optimism, Despair/Pessimism, Gratitude/Appreciation, Resentment/Bitterness, Compassion/Empathy, Indifference/Detachment, Excitement/Enthusiasm, Calm/Serenity, Confusion/Perplexity, Clarity/Understanding, Longing/Yearning, Satisfaction/Contentment, Frustration/Irritation, Awe/Reverence, Nostalgia/Wistfulness, Anticipation/Expectation, Relief/Release, Vulnerability/Exposure, Strength/Power, Isolation/Loneliness, Connection/Belonging, Trust/Faith, Suspicion/Doubt, Acceptance/Surrender, Resistance/Defiance

---

## Deployment

### Option 1: Local Development

```bash
python3 efv_api_server.py --host 0.0.0.0 --port 5000 --debug
```

### Option 2: Production with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 efv_api_server:create_app
```

### Option 3: Render.com (Recommended for Rapid Deployment)

1. Push repository to GitHub/GitLab
2. Create new Web Service on Render
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python efv_api_server.py --host 0.0.0.0 --port $PORT`
4. Set environment variables if needed
5. Deploy and point DNS CNAME to Render domain

### Option 4: Docker

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "efv_api_server.py", "--host", "0.0.0.0", "--port", "5000"]
```

```bash
docker build -t efv-api .
docker run -p 5000:5000 efv-api
```

---

## Integration Examples

### JavaScript/Browser

```javascript
// Fetch word of the day
fetch('https://tlvfoundation.org/efv/api/v1/word-of-day')
  .then(res => res.json())
  .then(data => console.log(data.word));

// Search
fetch('https://tlvfoundation.org/efv/api/v1/search?q=gratitude')
  .then(res => res.json())
  .then(data => console.log(data.results));
```

### Python

```python
import requests

# Get word of the day
response = requests.get('https://tlvfoundation.org/efv/api/v1/word-of-day')
word = response.json()

# Get specific word
word_detail = requests.get('https://tlvfoundation.org/efv/api/v1/word/ABHORRED')
```

### cURL

```bash
# Subscribe to RSS feed in your feed reader
https://tlvfoundation.org/efv/rss/daily-word.xml

# Download vocabulary
curl https://tlvfoundation.org/efv/export/csv?format=full > vocabulary.csv
```

---

## Performance & Caching

### Index Caching
- Indices loaded once at server startup
- LRU cache (512 entries) for Word of Day calculations
- Deterministic daily selection (same date = same word)

### Optimization Tips
- Cache API responses client-side (e.g., 24-hour TTL for word-of-day)
- Batch requests when fetching multiple words
- Use category and letter endpoints for filtered browsing
- Implement pagination for large result sets in your application

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "status": "error",
  "message": "Word not found: NONEXISTENT"
}
```

### Common Status Codes

- **200 OK** - Successful request
- **400 Bad Request** - Invalid query parameters
- **404 Not Found** - Word, category, or letter not found
- **500 Internal Server Error** - Server-side issue

---

## License & Attribution

This API and vocabulary are licensed under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)**.

### Non-Commercial Use (FREE)
✅ Personal use, education, research, non-profits, government

### Commercial Use (LICENSE REQUIRED)
For-profit businesses offering EFV-based services must obtain a commercial license.

**Contact:** licensing@tlvfoundation.org

### Attribution Required

When using the EFV API, please provide attribution:

```
Based on TriLateral Voice (TLV) Emotional and Feeling Vocabulary 
© 2025 The TriLateral Voice (TLV) Foundation Series
Licensed under CC BY-NC-SA 4.0
```

---

## Trademark Notice

**"TriLateral Voice"** and **"TLV"** are trademarks of The TriLateral Voice (TLV) Foundation Series.

You may reference TLV in descriptive text, but cannot use the names in product/service names without written permission.

**Contact:** info@tlvfoundation.org

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:
- Reporting issues
- Suggesting API improvements
- Contributing vocabulary enhancements
- Proposing feature additions

This is an early release (RC0001). We actively seek feedback from practitioners, developers, researchers, and community members.

---

## Technical Stack

- **Framework:** Flask 2.x (Python)
- **Server:** Gunicorn (production) or Flask dev server
- **Data Format:** JSON indices, CSV exports, RSS feeds
- **CORS:** Enabled for cross-origin browser requests
- **Caching:** LRU cache for performance
- **Versioning:** API v1, semantic versioning

### Requirements

```
Flask==2.3.0
flask-cors==4.0.0
feedgen==0.9.0
python-dateutil==2.8.2
```

---

## Roadmap

**RC0001 (Current)** - Core API with word-of-day, search, and export
**RC0002** - Advanced search filters, intensity ranges, cultural perspectives
**RC0003** - User accounts, personal word collections, annotation
**1.0** - Stability release, performance optimizations, expanded integrations

---

## Support & Contact

- **Issues & Discussions:** [GitHub Issues](https://github.com/your-repo/issues)
- **General Inquiries:** info@tlvfoundation.org
- **API Questions:** api@tlvfoundation.org
- **Commercial Licensing:** licensing@tlvfoundation.org

---

## Important Scope Clarification

**The EFV API documents emotional experience—it does not diagnose, treat, or provide mental health care.**

While EFV language can inform care and support authentic understanding, it **does not replace professional mental health services, medical treatment, or clinical therapy.**

If experiencing persistent emotional distress, thoughts of self-harm, trauma responses, or mental health crisis, please reach out to:
- Mental health professionals
- Crisis hotlines
- Trusted support networks
- Medical providers

---

## Foundational Principles

The TLV framework that powers EFV is grounded in three key axioms:

1. **A past we have survived is not a defect, it is a victory we need to claim.**
2. **Life is the reward for surviving our past.**
3. **No one can make you mad—it is an internal response to external input.**

These principles emphasize agency, resilience, and the recognition that emotional responses are internal processes influenced by—but not determined by—external events.

---

## Citation

If you use the EFV API in research or publications:

**APA Format:**
```
TLV Foundation Series. (2025). TriLateral Voice (TLV) Emotional and 
    Feeling Vocabulary API (Version RC0001). Retrieved from 
    https://tlvfoundation.org/efv. Licensed under CC BY-NC-SA 4.0.
```

**Bibtex:**
```bibtex
@software{efv_api_2025,
  author = {{TLV Foundation Series}},
  title = {TriLateral Voice (TLV) Emotional and Feeling Vocabulary API},
  version = {RC0001},
  year = {2025},
  url = {https://tlvfoundation.org/efv},
  license = {CC BY-NC-SA 4.0}
}
```

---

## Status

**Current Version:** RC0001 (Release Candidate)  
**Status:** Production-Ready (RC)  
**Last Updated:** January 01, 2026

This is an active development project. Feedback and contributions are welcome.

---

## Learn More

- [TriLateral Voice Framework](https://tlvfoundation.org)
- [TLV Communication Protocol](docs/TLV-Communication-Protocol.md)
- [EFV Vocabulary Documentation](docs/EFV-Vocabulary.md)
- [API Manifest](vocab/_indices/02_API_MANIFEST.json)

---

© 2025-2026 The TriLateral Voice (TLV) Foundation Series

Licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)

**Non-commercial use is free.** Commercial use requires a license.  
For details, email: licensing@tlvfoundation.org

**Trademarks:** "TriLateral Voice" and "TLV" are trademarks of The TriLateral Voice (TLV) Foundation Series.  
See trademark guidelines, email: info@tlvfoundation.org
