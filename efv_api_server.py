#!/usr/bin/env python3

"""
TriLateral Voice (TLV) Emotional and Feeling Vocabulary
REST API Server

Provides endpoints for:
- Word of the Day
- Random word selection
- Category/letter browsing
- Full-text search
- RSS feed generation
- CSV exports

Usage:
    pip install flask python-dateutil feedgen
    python efv_api_server.py
    
Then access:
    http://localhost:5000/api/v1/word-of-day
    http://localhost:5000/api/v1/word/random
    http://localhost:5000/api/v1/word/ABHORRED
    http://localhost:5000/api/v1/category/Disgust
    http://localhost:5000/rss/daily-word.xml
"""

import json
import random
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional
from functools import lru_cache
import hashlib
import sys

from flask import Flask, jsonify, request, Response, send_from_directory
from flask_cors import CORS
from feedgen.feed import FeedGenerator
import csv
from io import StringIO


def find_git_root(start_path: Path = None) -> Path:
    """
    Find the root of the Git repository by walking up the directory tree
    until a .git directory is found.
    """
    if start_path is None:
        start_path = Path(__file__).resolve().parent
    
    current = start_path.resolve()
    while current != current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    
    raise FileNotFoundError(
        f"Git repository root not found starting from {start_path}"
    )

class EFVDatabase:
    """Load and manage vocabulary data with portable path resolution."""
    
    def __init__(self, index_dir: Path = None):
        """
        Load indices from a directory.
        
        Args:
            index_dir: where to find 01_INDEX.json (defaults to <repo>/vocab/_indices)
        """
        if index_dir:
            # User provided explicit path
            self.index_dir = Path(index_dir).resolve()
        else:
            # Default: locate indices relative to repo root
            try:
                repo_root = find_git_root()
                self.index_dir = repo_root / "vocab/_indices"
            except FileNotFoundError:
                # Fallback: use script's sibling vocab/_indices
                self.index_dir = Path(__file__).resolve().parent / "vocab/_indices"

        self.index_data = None
        self.by_letter = {}
        self.by_category = {}
        self.all_words = {}

        self.load_indices()
    
    def load_indices(self):
        """Load JSON indices from self.index_dir."""
        index_file = self.index_dir / "01_INDEX.json"
        
        if not index_file.exists():
            raise FileNotFoundError(
                f"Index file not found: {index_file}\n"
                f"Make sure to run: python3 efv_index_generator.py"
            )

        print(f"📂 Loading indices from: {self.index_dir}")
        
        with open(index_file, "r", encoding="utf-8") as f:
            self.index_data = json.load(f)

        # Build lookups
        for word_data in self.index_data.get("all_words", []):
            word = word_data["word"].upper()
            self.all_words[word] = word_data

        # By letter
        for letter, words in self.index_data.get("by_letter", {}).items():
            self.by_letter[letter] = words

        # By category
        for category, words in self.index_data.get("by_category", {}).items():
            self.by_category[category] = words

        print(f"✓ Loaded {len(self.all_words)} words")
    
    @lru_cache(maxsize=512)
    def get_word_of_day(self, specific_date: Optional[date] = None) -> Dict:
        """Get deterministic word for specific date"""
        target_date = specific_date or date.today()
        
        # Use date as seed for reproducible daily word
        seed_str = target_date.isoformat()
        seed_hash = int(hashlib.md5(seed_str.encode()).hexdigest(), 16)
        
        words = self.index_data['all_words']
        selected = words[seed_hash % len(words)]
        
        return {
            'word': selected,
            'date': target_date.isoformat(),
            'total_words': len(words)
        }
    
    def get_random_word(self) -> Dict:
        """Get random word"""
        words = self.index_data['all_words']
        selected = random.choice(words)
        return selected
    
    def get_word(self, word_name: str) -> Optional[Dict]:
        """Get specific word"""
        return self.all_words.get(word_name.upper())
    
    def search_words(self, query: str) -> List[Dict]:
        """Search words by name or category"""
        query_lower = query.lower()
        results = []
        
        for word_data in self.index_data['all_words']:
            if (query_lower in word_data['word'].lower() or
                query_lower in word_data['category'].lower()):
                results.append(word_data)
        
        return results[:20]  # Limit to 20 results
    
    def get_category(self, category_name: str) -> List[Dict]:
        """Get all words in category"""
        for cat, words in self.index_data['by_category'].items():
            if category_name.lower() in cat.lower():
                return words
        return []
    
    def get_letter(self, letter: str) -> List[Dict]:
        """Get all words starting with letter"""
        return self.by_letter.get(letter.upper(), [])


def create_app(index_dir: Path = None) -> Flask:
    """Create Flask application with portable path resolution."""
    app = Flask(__name__)
    CORS(app)


    @app.route("/favicon.ico")
    def favicon():
        app_root = Path(__file__).resolve().parent
        # Assumes favicon.ico is in the same directory as efv_api_server.py
        return send_from_directory(
            app_root,
            "favicon.ico",
            mimetype="image/vnd.microsoft.icon",
        )

    try:
        db = EFVDatabase(index_dir)
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        return None

    # ========== ROUTES DEFINED HERE (inside create_app) ==========

    @app.route("/api/v1/word-of-day", methods=["GET"])
    def word_of_day():
        """Daily word with deterministic selection and manifest-aligned schema."""
        try:
            specific_date_str = request.args.get("date")
            specific_date = None
            if specific_date_str:
                specific_date = datetime.fromisoformat(specific_date_str).date()

            wotd_info = db.get_word_of_day(specific_date)
            word_data = wotd_info["word"]

            return jsonify(
                status="success",
                date=wotd_info["date"],
                total_words=wotd_info["total_words"],
                word=word_data.get("word"),
                category=word_data.get("category"),
                precision_level=word_data.get("precision_level"),
                somatic_integration=word_data.get("somatic_integration"),
                temporal_translation=word_data.get("temporal_translation"),
                cultural_bridge=word_data.get("cultural_bridge"),
                sections={
                    "1": "Etymology & Historical Development",
                    "2": "Contemporary Common Usage",
                    "3": "Precise Evocation Intent",
                    "4": "Conceptual Explanation",
                    "5": "Cultural Translation Contexts",
                    "6": "TLV Protocol Application",
                    "7": "Somatic Signature Documentation",
                },
            )
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    @app.route("/api/v1/word/random", methods=["GET"])
    def random_word():
        """Get random word"""
        try:
            word_data = db.get_random_word()
            return jsonify(
                status="success",
                word=word_data.get("word"),
                category=word_data.get("category"),
                precision_level=word_data.get("precision_level"),
            )
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    @app.route("/api/v1/word/<word_name>", methods=["GET"])
    def get_word(word_name):
        """Get specific word details"""
        try:
            word_data = db.get_word(word_name)
            if not word_data:
                return jsonify(
                    status="error",
                    message=f"Word not found: {word_name}",
                ), 404
            return jsonify(status="success", data=word_data)
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    @app.route("/api/v1/category/<category_name>", methods=["GET"])
    def get_category(category_name):
        """Get all words in category"""
        try:
            words = db.get_category(category_name)
            if not words:
                return jsonify(
                    status="error",
                    message=f"Category not found: {category_name}",
                ), 404
            return jsonify(
                status="success",
                category=category_name,
                word_count=len(words),
                words=[{"word": w.get("word"), "precision_level": w.get("precision_level")} for w in words],
            )
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    @app.route("/api/v1/letter/<letter>", methods=["GET"])
    def get_letter(letter):
        """Get all words starting with letter"""
        try:
            words = db.get_letter(letter)
            if not words:
                return jsonify(
                    status="error",
                    message=f"No words found for letter: {letter}",
                ), 404
            return jsonify(
                status="success",
                letter=letter.upper(),
                word_count=len(words),
                words=[{"word": w.get("word")} for w in words],
            )
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    @app.route("/api/v1/search", methods=["GET"])
    def search():
        """Search words by name or category"""
        try:
            query = request.args.get("q", "")
            if not query or len(query) < 2:
                return jsonify(
                    status="error",
                    message="Query must be at least 2 characters",
                ), 400

            results = db.search_words(query)
            return jsonify(
                status="success",
                query=query,
                result_count=len(results),
                results=[{"word": w.get("word"), "category": w.get("category")} for w in results],
            )
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    @app.route("/rss/daily-word.xml", methods=["GET"])
    def rss_feed():
        """RSS feed for daily word - FIXED with timezone-aware datetimes"""
        try:
            fg = FeedGenerator()
            fg.id("https://tlvfoundation.org/efv")
            fg.title("TLV Word of the Day")
            fg.link(href="https://tlvfoundation.org", rel="alternate")
            fg.description("Daily emotional and feeling vocabulary from TLV")
            fg.language("en")
            
            for i in range(30):
                target_date = date.today() - timedelta(days=i)
                wotd_info = db.get_word_of_day(target_date)
                word_data = wotd_info["word"]
                
                fe = fg.add_entry()
                fe.id(f"word-{target_date.isoformat()}")
                fe.title(f"Word of the Day: {word_data.get('word')}")
                fe.description(
                    f"{word_data.get('word')} | "
                    f"Category: {word_data.get('category', 'N/A')} | "
                    f"Precision Level: {word_data.get('precision_level', 'N/A')}"
                )
                
                # FIX: Create timezone-aware datetime (UTC)
                aware_datetime = datetime.combine(
                    target_date, 
                    datetime.min.time()
                ).replace(tzinfo=timezone.utc)
                
                fe.published(aware_datetime)
                fe.link(href=f"https://tlvfoundation.org/word/{word_data.get('word')}")
            
            return Response(fg.rss_str(pretty=True), mimetype="application/rss+xml")
        
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    @app.route("/export/csv", methods=["GET"])
    def export_csv():
        """Export vocabulary as CSV"""
        try:
            format_type = request.args.get("format", "full")
            output = StringIO()

            if format_type == "full":
                fieldnames = [
                    "word",
                    "letter",
                    "category",
                    "precision_level",
                    "etymology_summary",
                    "somatic_integration",
                    "temporal_translation",
                    "cultural_bridge",
                    "hash_value",
                ]
            elif format_type == "wotd":
                fieldnames = ["word", "category", "precision_level"]
            else:
                fieldnames = ["word", "category"]

            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()

            for word_data in db.index_data.get("all_words", []):
                row = {f: word_data.get(f, "") for f in fieldnames}
                writer.writerow(row)

            csv_content = output.getvalue()
            return Response(
                csv_content,
                mimetype="text/csv",
                headers={"Content-Disposition": "attachment; filename=efv_vocabulary.csv"},
            )
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    @app.route("/api/v1/metadata", methods=["GET"])
    def metadata():
        """Get API metadata"""
        try:
            return jsonify(
                status="success",
                api_version="1.0",
                total_words=len(db.all_words),
                categories=list(db.index_data.get("metadata", {}).get("categories", [])),
                letters=list(db.index_data.get("metadata", {}).get("letters", [])),
                endpoints={
                    "word_of_day": "/api/v1/word-of-day",
                    "random_word": "/api/v1/word/random",
                    "word_by_name": "/api/v1/word/{word}",
                    "words_by_category": "/api/v1/category/{category}",
                    "words_by_letter": "/api/v1/letter/{letter}",
                    "search": "/api/v1/search?q={query}",
                    "rss_feed": "/rss/daily-word.xml",
                    "csv_export": "/export/csv",
                },
            )
        except Exception as e:
            return jsonify(status="error", message=str(e)), 500

    @app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint"""
        return jsonify(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            words_loaded=len(db.all_words),
        )

    # ========== END ROUTES ==========

    return app


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="TLV EFV API Server"
    )
    parser.add_argument(
        "--index-dir",
        type=Path,
        default=None,
        help="Directory containing generated indices (defaults to <repo>/vocab/_indices)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to bind to"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("TLV Emotional and Feeling Vocabulary (EFV)")
    print("API Server")
    print("=" * 60)
    print()

    # Pass index_dir directly without pre-resolution
    app = create_app(args.index_dir)

    if app:
        print(f"✓ API Server ready!")
        print(f"🚀 Starting on {args.host}:{args.port}")
        print(f"📖 Visit http://{args.host}:{args.port}/api/v1/metadata for API info")
        print()
        print("Endpoints:")
        print(f"  - GET /api/v1/word-of-day       Daily word")
        print(f"  - GET /api/v1/word/random       Random word")
        print(f"  - GET /api/v1/word/<word>       Specific word")
        print(f"  - GET /api/v1/category/<cat>    Words by category")
        print(f"  - GET /api/v1/letter/<letter>   Words by letter")
        print(f"  - GET /api/v1/search?q=<query>  Search")
        print(f"  - GET /rss/daily-word.xml       RSS feed")
        print(f"  - GET /export/csv               CSV export")
        print(f"  - GET /api/v1/metadata          API metadata")
        print("=" * 60)
        print()

        app.run(host=args.host, port=args.port, debug=args.debug)
    else:
        print("❌ Failed to create app. Check index directory.")
        sys.exit(1)


if __name__ == "__main__":
    main()
