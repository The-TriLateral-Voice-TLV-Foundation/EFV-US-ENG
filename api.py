#!/usr/bin/env python3
"""
TLV Emotional and Feeling Vocabulary (EFV) API
===============================================
A RESTful API serving 999 emotion/feeling entries with six-dimensional
analysis, somatic signatures, intensity mappings, and cultural translations.

Run:  uvicorn api:app --reload --port 8000
Docs: http://localhost:8000/docs
"""

import json, os, glob
from pathlib import Path
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# ── Paths ────────────────────────────────────────────────────
BASE        = Path(__file__).resolve().parent
DATA_DIR    = BASE / "data"
ENTRIES_DIR = DATA_DIR / "entries"
INDICES_DIR = DATA_DIR / "indices"
LETTER_DIR  = DATA_DIR                       # efv-a.json … efv-z.json

# ── In-memory stores (populated on startup) ──────────────────
MASTER_INDEX: dict      = {}
ENTRIES_CACHE: dict     = {}                  # term → full entry dict
LETTER_CACHE: dict      = {}                  # letter → [term, …]
SOMATIC_INDEX: dict     = {}
INTENSITY_INDEX: dict   = {}

# ── App ──────────────────────────────────────────────────────
app = FastAPI(
    title="TLV Emotional & Feeling Vocabulary API",
    version="1.0.0",
    description="Access 999 emotions/feelings with etymology, somatic signatures, cultural translations, and more.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Data loader ──────────────────────────────────────────────
@app.on_event("startup")
def load_data():
    global MASTER_INDEX, SOMATIC_INDEX, INTENSITY_INDEX

    # 1. Master index
    mi_path = INDICES_DIR / "master_index.json"
    if mi_path.exists():
        with open(mi_path) as f:
            MASTER_INDEX.update(json.load(f))

    # 2. Somatic-region index
    sr_path = INDICES_DIR / "somatic_region.json"
    if sr_path.exists():
        with open(sr_path) as f:
            SOMATIC_INDEX.update(json.load(f))

    # 3. Intensity index
    int_path = INDICES_DIR / "intensity.json"
    if int_path.exists():
        with open(int_path) as f:
            INTENSITY_INDEX.update(json.load(f))

    # 4. Load every individual entry JSON
    for letter_dir in sorted(ENTRIES_DIR.iterdir()):
        if not letter_dir.is_dir():
            continue
        letter = letter_dir.name
        terms_for_letter = []
        for entry_file in sorted(letter_dir.glob("*.json")):
            with open(entry_file) as f:
                entry = json.load(f)
            term = entry.get("term", entry_file.stem)
            ENTRIES_CACHE[term.lower()] = entry
            terms_for_letter.append(term)
        LETTER_CACHE[letter] = terms_for_letter

    # Fallback: also load letter bundle files (efv-a.json …)
    for lf in sorted(LETTER_DIR.glob("efv-*.json")):
        with open(lf) as f:
            bundle = json.load(f)
        letter = bundle.get("letter", lf.stem.split("-")[-1])
        for entry in bundle.get("entries", []):
            term = entry.get("term", "").lower()
            if term and term not in ENTRIES_CACHE:
                ENTRIES_CACHE[term] = entry
        if letter not in LETTER_CACHE:
            LETTER_CACHE[letter] = bundle.get("terms", [])

    print(f"[EFV] Loaded {len(ENTRIES_CACHE)} entries across {len(LETTER_CACHE)} letters")


# ── Utility ──────────────────────────────────────────────────
def _clean(text: str) -> str:
    """Strip markdown-style prefixes like 'Language**: ' from values."""
    if not text:
        return text
    for prefix in ("Language**: ", "Meaning**: ", "Evolution**: ", "Shifts**: ",
                    "Definition**: ", "Usage**: ", "Experience**: ", "Response**: ",
                    "Concept**: ", "Context**: ", "Aspect**: ", "Spectrum**: ",
                    "Voice Usage**: ", "Requirements**: ", "Descriptors**: "):
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text


def _format_entry(entry: dict) -> dict:
    """Return a cleaned, API-friendly version of an entry."""
    dims = entry.get("six_dimensions", {})
    som = entry.get("somatic_signature", {})

    def _get(d, k):
        return _clean(d.get(k, "")) if isinstance(d.get(k), str) else d.get(k, "")

    return {
        "term": entry.get("term", ""),
        "intensity_range": entry.get("intensity_range", ""),
        "etymology": {
            "root_language":     _get(dims.get("etymology_and_history", {}), "root_language"),
            "original_meaning":  _get(dims.get("etymology_and_history", {}), "original_meaning"),
            "semantic_evolution": _get(dims.get("etymology_and_history", {}), "semantic_evolution"),
            "cultural_shifts":   _get(dims.get("etymology_and_history", {}), "cultural_shifts"),
        },
        "contemporary_usage": {
            "definition":     _get(dims.get("contemporary_usage", {}), "primary_definition"),
            "colloquial":     _get(dims.get("contemporary_usage", {}), "colloquial_usage"),
            "register":       dims.get("contemporary_usage", {}).get("register", ""),
        },
        "evocation": {
            "speaker_experience": _get(dims.get("precise_evocation", {}), "speaker_experience"),
            "listener_response":  _get(dims.get("precise_evocation", {}), "listener_response"),
            "authenticity":       _get(dims.get("precise_evocation", {}), "authenticity_markers"),
        },
        "conceptual": {
            "core_concept":      _get(dims.get("conceptual_explanation", {}), "core_concept"),
            "relational_context": _get(dims.get("conceptual_explanation", {}), "relational_context"),
            "temporal_aspect":    _get(dims.get("conceptual_explanation", {}), "temporal_aspect"),
            "intensity_spectrum": _get(dims.get("conceptual_explanation", {}), "intensity_spectrum"),
        },
        "cultural_translation": dims.get("cultural_translation", {}).get("framework_perspectives", {}),
        "tlv_application": {
            "speakers_voice":    _get(dims.get("tlv_application", {}), "usage_in_speakers_voice"),
            "emotional_voice":   _get(dims.get("tlv_application", {}), "usage_in_emotional_somatic_voice"),
            "precision_reqs":    _get(dims.get("tlv_application", {}), "precision_level_requirements"),
        },
        "somatic_signature": {
            "primary_region":   _get(som.get("physical_location", {}), "primary_region"),
            "sensation_quality": _get(som.get("sensation_quality", {}), "texture"),
        },
        "translations": entry.get("translations", {}),
        "has_4lang_verification": entry.get("has_4lang_verification", False),
        "meta": entry.get("_meta", {}),
    }


# ══════════════════════════════════════════════════════════════
#  ENDPOINTS
# ══════════════════════════════════════════════════════════════

@app.get("/")
def root():
    return FileResponse(BASE / "frontend" / "index.html")


@app.get("/api/stats")
def stats():
    """High-level statistics about the vocabulary."""
    mi = MASTER_INDEX
    return {
        "total_entries": mi.get("total_entries", len(ENTRIES_CACHE)),
        "isa_version":   mi.get("isa_version", "TLV-EFV-ISA-RC0001"),
        "letters":       sorted(LETTER_CACHE.keys()),
        "letter_counts": {k: len(v) for k, v in sorted(LETTER_CACHE.items())},
    }


@app.get("/api/letters/{letter}")
def get_letter(letter: str):
    """List all terms for a given letter."""
    letter = letter.lower()
    terms = LETTER_CACHE.get(letter)
    if terms is None:
        raise HTTPException(404, f"No entries for letter '{letter}'")
    entries_meta = []
    mi_entries = MASTER_INDEX.get("entries", {})
    for t in sorted(terms, key=str.lower):
        meta = mi_entries.get(t, {})
        entries_meta.append({
            "term": t,
            "intensity_range": meta.get("intensity_range", ""),
            "has_somatic": meta.get("has_somatic", True),
            "quality_tier": meta.get("quality_tier", 1),
        })
    return {"letter": letter, "count": len(terms), "entries": entries_meta}


@app.get("/api/entries/{term}")
def get_entry(term: str):
    """Full entry for a single emotion/feeling term."""
    entry = ENTRIES_CACHE.get(term.lower())
    if not entry:
        raise HTTPException(404, f"Entry '{term}' not found")
    return _format_entry(entry)


@app.get("/api/search")
def search(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(50, ge=1, le=200),
):
    """Search entries by term name (prefix / substring match)."""
    q_lower = q.lower()
    exact, prefix, contains = [], [], []
    for term in ENTRIES_CACHE:
        if term == q_lower:
            exact.append(term)
        elif term.startswith(q_lower):
            prefix.append(term)
        elif q_lower in term:
            contains.append(term)
    results = exact + sorted(prefix) + sorted(contains)
    results = results[:limit]
    mi_entries = MASTER_INDEX.get("entries", {})
    return {
        "query": q,
        "count": len(results),
        "results": [
            {
                "term": t,
                "intensity_range": mi_entries.get(t, {}).get("intensity_range", ""),
                "definition": _clean(
                    ENTRIES_CACHE[t]
                    .get("six_dimensions", {})
                    .get("contemporary_usage", {})
                    .get("primary_definition", "")
                ),
            }
            for t in results
        ],
    }


@app.get("/api/intensity/{range_str}")
def by_intensity(range_str: str):
    """Get all entries matching a given intensity range (e.g., '3-4')."""
    mi_entries = MASTER_INDEX.get("entries", {})
    matches = [
        {"term": t, "intensity_range": m.get("intensity_range", "")}
        for t, m in mi_entries.items()
        if m.get("intensity_range") == range_str
    ]
    return {"intensity_range": range_str, "count": len(matches), "entries": sorted(matches, key=lambda x: x["term"])}


@app.get("/api/random")
def random_entry():
    """Return a random entry."""
    import random
    term = random.choice(list(ENTRIES_CACHE.keys()))
    return _format_entry(ENTRIES_CACHE[term])


# ── Static frontend ──────────────────────────────────────────
app.mount("/static", StaticFiles(directory=str(BASE / "frontend")), name="static")
