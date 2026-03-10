<div align="center">

<!-- ═══════════════════════════════════════════════════════════
     TRILATERAL VOICE · EMOTIONAL & FEELING VOCABULARY
     Brand Identity v1.0 — Parchment · Violet · Gold
     ═══════════════════════════════════════════════════════════ -->

<img src="post-image-hori-2.jpg" alt="Trilateral Voice — Three voices. Complete communication." width="100%">

<br>

# Trilateral Voice · Emotional & Feeling Vocabulary

**Three voices. Complete communication.**

[![ISA Version](https://img.shields.io/badge/ISA-TLV--EFV--ISA--RC0001-574c6e?style=flat-square&labelColor=3e3955)](.)
[![Entries](https://img.shields.io/badge/Entries-999-c4a98b?style=flat-square&labelColor=574c6e)](.)
[![Dimensions](https://img.shields.io/badge/Dimensions-6-76678a?style=flat-square&labelColor=3e3955)](.)
[![License](https://img.shields.io/badge/License-TLV--EFV-9093a3?style=flat-square&labelColor=574c6e)](.)
[![Python](https://img.shields.io/badge/Python-3.9%2B-c4a98b?style=flat-square&logo=python&logoColor=f5eedf&labelColor=3e3955)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-76678a?style=flat-square&logo=fastapi&logoColor=f5eedf&labelColor=574c6e)](https://fastapi.tiangolo.com)

---

A full-stack application providing API access and a beautiful frontend for exploring<br>
**999 emotions and feelings**, each analyzed across six dimensions.

*Map the conversation you're actually having.*

</div>

---

## ◉ Quick Start

```bash
# 1. Clone / download this project
# 2. Place your data files in the project root
# 3. Run setup:
chmod +x setup.sh
./setup.sh
```

> The app launches at **http://localhost:8000**

---

## ◎ Architecture

```
tlv-efv/
│
├── api.py                          # FastAPI backend
├── setup.sh                        # One-command setup & launch
├── requirements.txt                # Python dependencies
│
├── frontend/
│   └── index.html                  # Single-page frontend app (TLV branded)
│
└── data/
    ├── efv-a.json … efv-z.json     # Letter bundle files
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

---

## ◈ API Reference

| Method | Endpoint | Description |
|:------:|:---------|:------------|
| `GET` | `/api/stats` | Vocabulary statistics & letter counts |
| `GET` | `/api/letters/{letter}` | List all terms for a given letter |
| `GET` | `/api/entries/{term}` | Full entry with all 6 dimensions |
| `GET` | `/api/search?q=...` | Search by term name (prefix / substring) |
| `GET` | `/api/intensity/{range}` | Filter by intensity range (e.g., `3-4`) |
| `GET` | `/api/random` | Random entry |

<details>
<summary><b>Example: Get Entry</b></summary>

<br>

```bash
curl http://localhost:8000/api/entries/joy | python -m json.tool
```

**Response Shape**

```json
{
  "term": "joy",
  "intensity_range": "5-6",
  "etymology": {
    "root_language": "Latin \"gaudia\" ...",
    "original_meaning": "...",
    "semantic_evolution": "...",
    "cultural_shifts": "..."
  },
  "contemporary_usage": {
    "definition": "...",
    "colloquial": "...",
    "register": "..."
  },
  "evocation": { "..." },
  "conceptual": { "..." },
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
  "tlv_application": { "..." }
}
```

</details>

---

## 📖 Six Dimensions

Each of the 999 entries is analyzed across a complete analytical framework:

| Dimension | What It Captures |
|:----------|:-----------------|
| **Etymology & History** | Root language, original meaning, semantic evolution, cultural shifts |
| **Contemporary Usage** | Modern definition, colloquial register, contextual nuance |
| **Precise Evocation** | Speaker experience, listener response, communicative intent |
| **Conceptual Framework** | Core concept, relational context, temporal aspect, intensity spectrum |
| **Cultural Translation** | Western, Eastern, Indigenous, Clinical, Spiritual, Philosophical lenses |
| **TLV Application** | Speaker's voice mapping, emotional-somatic voice, precision requirements |

---

## 🫀 Somatic Signatures

Every entry includes body-mapped somatic data:

- **Primary Body Region** — Where the emotion physically manifests
- **Sensation Quality** — The texture and character of the felt experience

---

## 🌍 Cultural Bridges

Translations and cultural framings across **six worldview perspectives**, ensuring the vocabulary serves global, cross-cultural communication — not just Western clinical categories.

---

## 🌡️ Intensity Ranges

Calibrated **1–10 intensity mappings** for each entry, enabling precise emotional granularity in both clinical and conversational contexts.

---

## ✨ Frontend Features

- **Alphabet navigation** with entry counts per letter
- **Live search** with debounced autocomplete
- **Random entry** button for discovery
- **Detailed entry view** showing all six dimensions
- **Dark / Light theme** toggle — both fully TLV-branded
- **Responsive** layout for desktop and mobile
- **Accessible** — WCAG AA contrast, keyboard navigation, semantic HTML

---

## ⚙️ Technology Stack

| Layer | Technology |
|:------|:-----------|
| **Backend** | Python 3.9+ · FastAPI · Uvicorn |
| **Frontend** | Vanilla HTML / CSS / JS — no build step |
| **Data** | JSON files — no database required |
| **Brand System** | TLV Design Tokens v1.0 — IBM Plex Serif + Sans |

---

## 📦 Requirements

```
fastapi>=0.100.0
uvicorn[standard]>=0.23.0
aiofiles>=23.0
python-multipart>=0.0.6
```

---

## 🏛️ Data Schema

Each entry contains:

- **Six Dimensions** — Etymology, contemporary usage, precise evocation, conceptual explanation, cultural translation, TLV application
- **Somatic Signature** — Primary body regions, sensation quality descriptors
- **Intensity Range** — Calibrated 1-10 scale
- **Translations** — French, Spanish, German, Mandarin (where available)
- **Quality Metadata** — ISA version, conversion tier, field completeness

---

<div align="center">

<br>

**Trilateral Voice Foundation**

*Clarity is care.*

<br>

[![TLV Foundation](https://img.shields.io/badge/TLV-Foundation-574c6e?style=for-the-badge&labelColor=3e3955)](https://github.com/The-TriLateral-Voice-TLV-Foundation)
[![Bluesky](https://img.shields.io/badge/Bluesky-@trilateralvoice-76678a?style=for-the-badge&logo=bluesky&logoColor=f5eedf&labelColor=574c6e)](https://bsky.app/profile/trilateralvoice.bsky.social)

---

<sub>TLV-EFV-ISA-RC0001 · 999 Entries · Brand System v1.0 · © 2026 The Trilateral Voice Foundation</sub>

</div>
