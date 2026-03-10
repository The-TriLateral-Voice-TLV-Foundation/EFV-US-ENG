# TLV Emotional & Feeling Vocabulary (EFV)

A full-stack application providing API access and a beautiful frontend for exploring **999 emotions and feelings**, each analyzed across six dimensions.

## Quick Start

```bash
# 1. Clone/download this project
# 2. Place your data files in the project root
# 3. Run setup:
chmod +x setup.sh
./setup.sh
```

The app launches at **http://localhost:8000**

## Architecture

```
tlv-efv/
├── api.py                 # FastAPI backend
├── setup.sh               # One-command setup & launch
├── requirements.txt       # Python dependencies
├── frontend/
│   └── index.html         # Single-page frontend app
└── data/
    ├── efv-a.json … efv-z.json    # Letter bundle files
    ├── entries/
    │   ├── a/
    │   │   ├── abhorred.json
    │   │   ├── absorbed.json
    │   │   └── …
    │   ├── b/ … z/
    └── indices/
        ├── master_index.json
        ├── intensity.json
        └── somatic_region.json
```

## API Endpoints

| Method | Endpoint                  | Description                              |
|--------|---------------------------|------------------------------------------|
| GET    | `/api/stats`              | Vocabulary statistics & letter counts    |
| GET    | `/api/letters/{letter}`   | List all terms for a letter              |
| GET    | `/api/entries/{term}`     | Full entry with all 6 dimensions         |
| GET    | `/api/search?q=...`       | Search by term name (prefix/substring)   |
| GET    | `/api/intensity/{range}`  | Filter by intensity range (e.g., "3-4")  |
| GET    | `/api/random`             | Random entry                             |

### Example: Get Entry

```bash
curl http://localhost:8000/api/entries/joy | python -m json.tool
```

### Response Shape

```json
{
  "term": "joy",
  "intensity_range": "5-6",
  "etymology": {
    "root_language": "Latin "gaudia" ...",
    "original_meaning": "...",
    "semantic_evolution": "...",
    "cultural_shifts": "..."
  },
  "contemporary_usage": {
    "definition": "...",
    "colloquial": "...",
    "register": "..."
  },
  "evocation": { ... },
  "conceptual": { ... },
  "cultural_translation": {
    "western": "...",
    "eastern": "...",
    "indigenous": "...",
    "clinical": "...",
    "spiritual": "...",
    "philosophical": "..."
  },
  "somatic_signature": {
    "primary_region": "heart, chest ...",
    "sensation_quality": "..."
  },
  "translations": { "fr": "...", "es": "...", "de": "...", "zh": "..." },
  "tlv_application": { ... }
}
```

## Frontend Features

- **Alphabet navigation** with entry counts per letter
- **Live search** with debounced autocomplete
- **Random entry** button for discovery
- **Detailed entry view** showing all six dimensions:
  - Etymology & History
  - Somatic Signature (body mapping)
  - Precise Evocation
  - Conceptual Framework
  - Cultural Translation (6 perspectives)
  - TLV Application guidance
- **Dark theme** optimized for readability
- **Responsive** layout for desktop and mobile

## Data Schema

Each entry contains:

- **Six Dimensions**: Etymology, contemporary usage, precise evocation, conceptual explanation, cultural translation, TLV application
- **Somatic Signature**: Primary body regions, sensation quality descriptors
- **Intensity Range**: Calibrated 1-10 scale
- **Translations**: French, Spanish, German, Mandarin (where available)
- **Quality Metadata**: ISA version, conversion tier, field completeness

## Technology Stack

- **Backend**: Python 3.9+ / FastAPI / Uvicorn
- **Frontend**: Vanilla HTML/CSS/JS (no build step)
- **Data**: JSON files (no database required)

## Requirements

```
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
aiofiles>=23.0
python-multipart>=0.0.6
```

## License

TLV-EFV-ISA-RC0001
