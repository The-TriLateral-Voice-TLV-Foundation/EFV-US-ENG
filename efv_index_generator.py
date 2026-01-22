#!/usr/bin/env python3
"""
TriLateral Voice (TLV) Emotional and Feeling Vocabulary (EFV) 
Auto-Index and TOC Generator

Generates comprehensive indices, tables of contents, and searchable metadata
for the EFV vocabulary files (a.json through z.json).

Supports:
- Auto-indexing of all vocabulary entries
- TOC generation at multiple levels
- JSON metadata for API integration
- CSV exports for Word of the Day, RSS feeds
- Watch mode for continuous updates

Usage:
    python efv_index_generator.py                    # Generate indices
    python efv_index_generator.py --watch           # Watch for changes
    python efv_index_generator.py --export api      # Export for API
    python efv_index_generator.py --format csv      # Export as CSV
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
import hashlib
import argparse
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import re
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler





@dataclass
class WordMetadata:
    """Metadata for each word entry"""
    word: str
    letter: str
    category: str
    precision_level: str
    somatic_integration: str
    temporal_translation: str
    cultural_bridge: str
    etymology_summary: str
    file_path: str
    last_updated: str
    hash_value: str  # For change detection


@dataclass
class IndexEntry:
    """Single entry in the index"""
    word: str
    letter: str
    category: str
    section_numbers: List[int]  # Which sections exist [1-7]
    metadata_hash: str


from pathlib import Path

class EFVIndexGenerator:
    """Main generator class for EFV indexing and metadata"""
    
    def __init__(self, base_directory: Path = None, output_directory: Path = None):
        # anchor at script directory
        script_dir = Path(__file__).resolve().parent

        # base_dir: <repo>/vocab by default
        self.base_dir = Path(base_directory) if base_directory else (script_dir / "vocab")

        # if caller provided an output_directory, normalize it
        if output_directory is not None:
            self.output_dir = Path(output_directory)
        else:
            # default: <repo>/vocab/_indices
            self.output_dir = self.base_dir / "_indices"

        # ensure directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        self.words_by_letter: Dict[str, List[str]] = {}
        self.words_by_category: Dict[str, List[str]] = {}
        self.all_metadata: List[WordMetadata] = []
        self.index_manifest: Dict = {}
        self.canonical_categories: List[str] = []  # Track ALL unique categories found
     
        
    def scan_vocabulary_files(self) -> Dict[str, Dict]:
        """Scan all JSON files and extract word entries"""
        print(f"🔍 Scanning vocabulary files in {self.base_dir}...")
        
        vocabulary = {}
        json_files = sorted(self.base_dir.glob("[a-z].json"))
        
        if not json_files:
            print(f"⚠️  No JSON files found in {self.base_dir}")
            return vocabulary
        
        for json_file in json_files:
            letter = json_file.stem.upper()
            print(f"  Processing {json_file.name}...", end=" ")
            
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Extract words from JSON structure
                words = self._extract_words_from_json(data)
                vocabulary[letter] = {
                    'file': json_file,
                    'words': words,
                    'file_size': json_file.stat().st_size,
                    'last_modified': datetime.fromtimestamp(
                        json_file.stat().st_mtime
                    ).isoformat()
                }
                
                print(f"✓ ({len(words)} words)")
                
            except json.JSONDecodeError as e:
                print(f"✗ JSON error: {e}")
            except Exception as e:
                print(f"✗ Error: {e}")
        
        return vocabulary
    
    def _extract_words_from_json(self, data: dict) -> List[Dict]:
        """Extract word entries from nested JSON structure"""
        words = []
        
        # Recursive function to find word entries
        def find_words(node, path=[]):
            if isinstance(node, dict):
                # Check if this is a word entry (has level 3 and content)
                if node.get('level') == 3 and node.get('type') == 'subsection':
                    title = node.get('title', '')
                    content = node.get('content', '')
                    children = node.get('children', [])
                    
                    words.append({
                        'word': title,
                        'category': self._extract_category(content),
                        'precision_level': self._extract_field(content, 'Precision Level'),
                        'somatic_integration': self._extract_field(content, 'Somatic Integration Required'),
                        'temporal_translation': self._extract_field(content, 'Temporal Translation Required'),
                        'cultural_bridge': self._extract_field(content, 'Cultural Bridge Integration'),
                        'sections': self._count_sections(children),
                        'content_preview': content[:200] if content else ''
                    })
                
                # Recurse into children
                for child in node.get('children', []):
                    find_words(child, path + [node.get('title', '')])
            
            elif isinstance(node, list):
                for item in node:
                    find_words(item, path)
        
        find_words(data)
        return words
    
    def _extract_category(self, content: str) -> str:
        """Extract category from content"""
        match = re.search(r'\*\*Category\*\*:\s*(.+?)(?:\n|$)', content)
        return match.group(1).strip() if match else 'Uncategorized'
    
    def _extract_field(self, content: str, field_name: str) -> str:
        """Extract specific field from content"""
        pattern = rf'\*\*{field_name}\*\*:\s*(.+?)(?:\n|$)'
        match = re.search(pattern, content)
        return match.group(1).strip() if match else 'Not specified'

    def analyze_categories(self) -> Dict[str, str]:
        """
        Analyze all unique categories in the actual vocabulary.
        Returns mapping of actual → canonical category.
        """
        actual_to_canonical = {}
        
        for metadata in self.all_metadata:
            actual_cat = metadata.category
            
            if actual_cat not in actual_to_canonical:
                # Try to find the canonical match
                canonical = self._find_canonical_category(actual_cat)
                actual_to_canonical[actual_cat] = canonical
        
        return actual_to_canonical

    def _find_canonical_category(self, actual: str) -> str:
        """Map an actual category string to the closest canonical value."""
        actual_lower = (actual or "").strip().lower()
        if not actual_lower:
            return "Uncategorized"

        # Normalize everything to strings so we support both Enum members and raw strings
        candidates = [c.value if hasattr(c, "value") else str(c) for c in self.canonical_categories]

        # 1) Exact match
        for cat in candidates:
            if cat.lower() == actual_lower:
                return cat

        # 2) Match primary part before '/'
        for cat in candidates:
            primary = cat.split("/", 1)[0].strip().lower()
            if primary and primary in actual_lower:
                return cat

        # 3) Fuzzy word overlap
        for cat in candidates:
            words = [w.strip() for w in cat.lower().replace("/", " ").split()]
            if any(w and w in actual_lower for w in words):
                return cat

        return "Uncategorized"

    def save_category_mapping(self, mapping: Dict[str, str]) -> None:
        """Save the actual → canonical category mapping for reference."""
        mapping_file = self.output_dir / "CATEGORY_MAPPING.csv"
        
        import csv

        with open(mapping_file, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["actual_category", "canonical_category"])
            writer.writeheader()
            
            for actual, canonical in sorted(mapping.items()):
                writer.writerow({
                    "actual_category": actual,
                    "canonical_category": canonical,
                })
        
        print(f"  ✓ {mapping_file.name} (mapping reference for {len(mapping)} variations)")


    def _count_sections(self, children: List) -> List[int]:
        """Count which sections exist in word entry"""
        sections = []
        for i, child in enumerate(children, 1):
            if child.get('type') == 'item':
                sections.append(i)
        return sections
    
    def generate_metadata(self, vocabulary: Dict) -> None:
        """Generate metadata for all words, building canonical category list"""
        print("\n📝 Generating metadata...")
        
        for letter, letter_data in vocabulary.items():
            self.words_by_letter[letter] = []
            
            for word_data in letter_data['words']:
                word = word_data['word']
                self.words_by_letter[letter].append(word)
                
                # Organize by category
                category = word_data['category']

                # Add to category index
                if category not in self.words_by_category:
                    self.words_by_category[category] = []
                    self.canonical_categories.append(category)  # Track as we discover
                
                self.words_by_category[category].append(word)
                
                # Create metadata record
                metadata = WordMetadata(
                    word=word,
                    letter=letter,
                    category=category,
                    precision_level=word_data.get("precision_level", "Not specified"),
                    somatic_integration=word_data.get("somatic_integration", "Not specified"),
                    temporal_translation=word_data.get("temporal_translation", "Not specified"),
                    cultural_bridge=word_data.get("cultural_bridge", "Not specified"),
                    etymology_summary=word_data.get("content_preview", ""),
                    file_path=letter_data["file"].name,
                    last_updated=letter_data["last_modified"],
                    hash_value=self._compute_hash(word_data),
                )
                self.all_metadata.append(metadata)

        # Sort canonical categories for consistent output
        self.canonical_categories = sorted(set(self.canonical_categories))
              
        print(f"✓ Generated metadata for {len(self.all_metadata)} words")
        print(f"✓ Found {len(self.canonical_categories)} unique categories in vocabulary") 
    
    def _compute_hash(self, data: dict) -> str:
        """Compute hash of word data for change detection"""
        json_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(json_str.encode()).hexdigest()[:16]
    
    def generate_toc(self) -> str:
        """Generate comprehensive table of contents using canonical categories"""
        print("📑 Generating table of contents...")
        
        toc_lines = [
            "# TriLateral Voice (TLV) Emotional and Feeling Vocabulary",
            "## Table of Contents",
            "",
            "---",
            "",
            "**Last Updated:** " + datetime.now().isoformat(),
            "",
            "---",
            "",
            "### Quick Navigation",
            ""
        ]
        
        # By Letter summary/index (NEW) ADDS ".lower"
        toc_lines.append("### By Letter")
        for letter in sorted(self.words_by_letter.keys()):
            count = len(self.words_by_letter[letter])
            toc_lines.append(f"- [{letter}](#{letter.lower()}) - {count} words")
        toc_lines.append("")

        # Category index (OLD)
        toc_lines.append("#### By Category")
        for category in sorted(self.words_by_category.keys()):
            count = len(self.words_by_category[category])
            toc_lines.append(f"- [{category}](#{category.lower().replace('/', '-')}) - {count} words")
        
        toc_lines.append("")
        toc_lines.append("---")
        toc_lines.append("")

        # By Category summary (using canonical Category enum) (NEW)
        # toc_lines.append("### By Category")

        # Sort canonical categories for consistent output
        # self.canonical_categories = sorted(set(self.canonical_categories))

        # for category_enum in sorted(self.canonical_categories, key=lambda c: c.value):
        #     # Get count from words_by_category if it exists, else 0
        #     category_display = category_enum.value  # e.g., "Joy/Happiness"
        #     count = len(self.words_by_category.get(category_display, []))
            
        #     # Create anchor-safe slug for link
        #     anchor = category_display.lower().replace("/", "-").replace(" ", "-")
        #     toc_lines.append(f"- [{category_display}](#{anchor}) - {count} words")
        
        # toc_lines.append("")
        # toc_lines.append("---")
        # toc_lines.append("")

        # Detailed letter sections
        toc_lines.append("## Words by Letter")
        toc_lines.append("")
        
        for letter in sorted(self.words_by_letter.keys()):
            words = sorted(self.words_by_letter[letter])
            toc_lines.append(f"### {letter}")
            toc_lines.append("")
            for i, word in enumerate(words, 1):
                toc_lines.append(f"{i}. {word}")
            toc_lines.append("")

        toc_lines.append("---")
        toc_lines.append("")

        # Category sections (OLD)
        toc_lines.append("## Words by Category")
        toc_lines.append("")
        
        for category in sorted(self.words_by_category.keys()):
            words = sorted(self.words_by_category[category])
            safe_category = category.lower().replace('/', '-').replace(' ', '-')
            toc_lines.append(f"### {category}")
            toc_lines.append("")
            for i, word in enumerate(words, 1):
                toc_lines.append(f"{i}. {word}")
            toc_lines.append("")
        
        toc_lines.append("---")
        toc_lines.append("")

        # Categories with all canonical entries (even empty ones) (NEW)
        # toc_lines.append("## Words by Category")
        # toc_lines.append("")

        # for category_enum in sorted(self.canonical_categories, key=lambda c: c.value):
        #     category_display = category_enum.value
        #     words = self.words_by_category.get(category_display, [])
            
        #     toc_lines.append(f"### {category_display}")
        #     toc_lines.append("")
            
        #     if words:
        #         for i, word in enumerate(sorted(words), 1):
        #             toc_lines.append(f"{i}. {word}")
        #     else:
        #         toc_lines.append("*No words in this category yet.*")
            
        #     toc_lines.append("")

        # toc_lines.append("---")
        # toc_lines.append("")

        # Vocabulary Statistics
        toc_lines.append("## Vocabulary Statistics")
        toc_lines.append("")
        toc_lines.append(f"- **Total Words:** {len(self.all_metadata)}")
        toc_lines.append(f"- **Total Letters:** {len(self.words_by_letter)}")
        toc_lines.append(f"- **Total Categories (Defined):** {len(self.canonical_categories)}")
        toc_lines.append(f"- **Total Categories (With Words):** {len(self.words_by_category)}")
        toc_lines.append(f"- **Generated:** {datetime.now().isoformat()}")
        toc_lines.append("")
        
        return "\n".join(toc_lines)
    
    def generate_index_json(self) -> Dict:
        """Generate searchable JSON index"""
        print("🔍 Generating JSON indices...")
        
        index = {
            'metadata': {
                'title': 'TLV Emotional and Feeling Vocabulary Index',
                'version': '1.0',
                'generated': datetime.now().isoformat(),
                'total_words': len(self.all_metadata),
                'letters': list(sorted(self.words_by_letter.keys())),
                'categories': list(sorted(self.words_by_category.keys()))
            },
            'by_letter': {},
            'by_category': {},
            'by_precision': {},
            'all_words': []
        }
        
        # Organize by letter
        for letter in sorted(self.words_by_letter.keys()):
            words = [self._find_metadata(w) for w in self.words_by_letter[letter]]
            index['by_letter'][letter] = [asdict(w) for w in words]
        
        # Organize by category
        for category in sorted(self.words_by_category.keys()):
            words = [self._find_metadata(w) for w in self.words_by_category[category]]
            index['by_category'][category] = [asdict(w) for w in words]
        
        # Organize by precision level
        precision_levels = set(m.precision_level for m in self.all_metadata)
        for level in sorted(precision_levels):
            words = [m for m in self.all_metadata if m.precision_level == level]
            index['by_precision'][level] = [asdict(w) for w in words]
        
        # All words flat
        index['all_words'] = [asdict(m) for m in sorted(
            self.all_metadata, key=lambda x: x.word
        )]
        
        return index
    
    def _find_metadata(self, word: str) -> Optional[WordMetadata]:
        """Find metadata for a word"""
        for m in self.all_metadata:
            if m.word.upper() == word.upper():
                return m
        return None
    
    def generate_api_manifest(self) -> Dict:
        """Generate manifest for API access using canonical categories"""
        print("📡 Generating API manifest...")

        categories_list = [
            {
                "name": category,
                "word_count": len(self.words_by_category.get(category, [])),
            }
            for category in self.canonical_categories
        ]

        manifest = {
            'api_version': '1.0',
            'generated': datetime.now().isoformat(),
            'endpoints': {
                'word_of_day': '/api/v1/word-of-day',
                'random_word': '/api/v1/word/random',
                'word_by_name': '/api/v1/word/{word}',
                'words_by_category': '/api/v1/category/{category}',
                'words_by_letter': '/api/v1/letter/{letter}',
                'search': '/api/v1/search?q={query}',
                'rss_feed': '/rss/daily-word.xml'
            },
            'word_count': len(self.all_metadata),
            'categories_canonical': self.canonical_categories,  # Full canonical list
            'letters': sorted(self.words_by_letter.keys()),
            "categories": categories_list,  # Complete list from actual vocabulary
            "category_count": len(self.canonical_categories),
            'response_format': {
                'word': 'string - word title',
                'category': 'string - emotional category',
                'precision_level': 'string - precision classification',
                'somatic_integration': 'string - somatic requirement',
                'temporal_translation': 'string - temporal translation',
                'cultural_bridge': 'string - cultural bridge requirement',
                'sections': {
                    '1': 'Etymology & Historical Development',
                    '2': 'Contemporary Common Usage',
                    '3': 'Precise Evocation Intent',
                    '4': 'Conceptual Explanation',
                    '5': 'Cultural Translation Contexts',
                    '6': 'TLV Protocol Application',
                    '7': 'Somatic Signature Documentation'
                }
            }
        }
        
        return manifest
    
    def generate_csv_export(self, output_format: str = 'full') -> str:
        """Generate CSV export for Word of Day, RSS feeds, etc."""
        print(f"📊 Generating CSV export ({output_format})...")
        
        import csv
        from io import StringIO
        
        output = StringIO()
      # REMOVED: ", 'file_path', 'last_updated', 'hash_value'""
        if output_format == 'full':
            fieldnames = [
                "word",
                "letter",
                "category",
                "precision_level",
                "etymology_summary",
                "content",
                "somatic_integration",
                "temporal_translation",
                "cultural_bridge",
                "filepath",
                "last_updated",
                "hash_value",
            ]
        elif output_format == "wotd":
            # Word of the Day (full metadata profile, single row per word)
            fieldnames = [
                "word",
                "letter",
                "category",
                "precision_level",
                "etymology_summary",
                "title",
                "content",
                "somatic_integration",
                "title",
                "content",
                "temporal_translation",
                "title",
                "content",
                "cultural_bridge",
                "title",
                "content",
                # "filepath",
                "last_updated",
                "hash_value",
            ]

        elif output_format == 'rss':  # RSS feed
            fieldnames = ['word', 'category', 'etymology_summary', 'date']
        
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        
        for metadata in sorted(self.all_metadata, key=lambda x: x.word):
            row = {k: v for k, v in asdict(metadata).items() if k in fieldnames}
            writer.writerow(row)

            if output_format == 'full':
                writer.writerow(asdict(metadata))
            elif output_format == 'wotd':
                writer.writerow({
                    'word': metadata.word,
                    'category': metadata.category,
                    'precision_level': metadata.precision_level,
                    'etymology_summary': metadata.etymology_summary
                })
            elif output_format == 'rss':
                writer.writerow({
                    'word': metadata.word,
                    'category': metadata.category,
                    'etymology_summary': metadata.etymology_summary,
                    'date': metadata.last_updated
                })
        
        return output.getvalue()
    
    def save_outputs(self, vocabulary: Dict) -> None:
        """Save all generated files"""
        print("\n💾 Saving outputs...")
        
        category_mapping = self.analyze_categories()
        self.save_category_mapping(category_mapping)

        # Save TOC
        toc_content = self.generate_toc()
        toc_file = self.output_dir / "00_TABLE_OF_CONTENTS.md"
        toc_file.write_text(toc_content, encoding='utf-8')
        print(f"  ✓ {toc_file.name}")
        
        # Save JSON index
        index_json = self.generate_index_json()
        index_file = self.output_dir / "01_INDEX.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_json, f, indent=2, ensure_ascii=False)
        print(f"  ✓ {index_file.name}")
        
        # Save API manifest
        api_manifest = self.generate_api_manifest()
        api_file = self.output_dir / "02_API_MANIFEST.json"
        with open(api_file, 'w', encoding='utf-8') as f:
            json.dump(api_manifest, f, indent=2, ensure_ascii=False)
        print(f"  ✓ {api_file.name}")
        
        # Save CSV exports
        csv_full = self.generate_csv_export('full')
        csv_file = self.output_dir / "03_VOCABULARY_FULL.csv"
        csv_file.write_text(csv_full, encoding='utf-8')
        print(f"  ✓ {csv_file.name}")
        
        csv_wotd = self.generate_csv_export('wotd')
        wotd_file = self.output_dir / "04_WORD_OF_DAY.csv"
        wotd_file.write_text(csv_wotd, encoding='utf-8')
        print(f"  ✓ {wotd_file.name}")
        
        csv_rss = self.generate_csv_export('rss')
        rss_file = self.output_dir / "05_RSS_FEED_DATA.csv"
        rss_file.write_text(csv_rss, encoding='utf-8')
        print(f"  ✓ {rss_file.name}")
        
        # Manifest File and Save
        manifest_file = self.output_dir / "MANIFEST.json"
        # self.index_manifest = {
        #     'generated': datetime.now().isoformat(),
        #     'files': {
        #         'table_of_contents': str(toc_file),
        #         'index_json': str(index_file),
        #         'api_manifest': str(api_file),
        #         'vocabulary_csv': str(csv_file),
        #         'word_of_day_csv': str(wotd_file),
        #         'rss_feed_csv': str(rss_file)
        #     },
        self.index_manifest = {
            'generated': datetime.now().isoformat(),
            'files': {
                'table_of_contents': toc_file.name,
                'index_json': index_file.name,
                'api_manifest': api_file.name,
                'vocabulary_csv': csv_file.name,
                'word_of_day_csv': wotd_file.name,
                'rss_feed_csv': rss_file.name
            },
            'statistics': {
                'total_words': len(self.all_metadata),
                'total_letters': len(self.words_by_letter),
                'total_categories': len(self.words_by_category),
                # 'total_categories_defined': len(Category),
                'total_categories_with_words': len(self.words_by_category),
                'vocabulary_files': len(vocabulary)
            }
        }
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(self.index_manifest, f, indent=2)
        print(f"  ✓ {manifest_file.name}")
    
    def run(self) -> None:
        """Main execution"""
        print("=" * 60)
        print("TLV Emotional and Feeling Vocabulary (EFV)")
        print("Auto-Index and TOC Generator")
        print("=" * 60)
        print()
        
        vocab = self.scan_vocabulary_files()
        if vocab:
            self.generate_metadata(vocab)
            self.save_outputs(vocab)
            
            print()
            print("=" * 60)
            print("✅ Index generation complete!")
            print(f"📁 Output directory: {self.output_dir}")
            print("=" * 60)
        else:
            print("❌ No vocabulary files found. Cannot proceed.")
            sys.exit(1)


class VocabularyWatcher(FileSystemEventHandler):
    """Watch for changes to vocabulary files"""
    
    def __init__(self, generator: EFVIndexGenerator):
        self.generator = generator
        self.cooldown = 2  # seconds
        self.last_run = 0
    
    def on_modified(self, event):
        if event.src_path.endswith('.json'):
            current_time = time.time()
            if current_time - self.last_run > self.cooldown:
                print(f"\n📝 Change detected: {Path(event.src_path).name}")
                self.generator.run()
                self.last_run = current_time


def main():
    parser = argparse.ArgumentParser(
        description='TLV Emotional Vocabulary Index Generator'
    )
    parser.add_argument(
        '--base-dir',
        type=Path,
        default=None,
        help='Base directory containing vocabulary files'
    )
    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help='Output directory for indices'
    )
    parser.add_argument(
        '--watch',
        action='store_true',
        help='Watch for file changes and auto-regenerate'
    )
    parser.add_argument(
        '--export',
        choices=['api', 'csv', 'json', 'toc'],
        help='Export specific format'
    )
    parser.add_argument(
        '--format',
        choices=['full', 'wotd', 'rss'],
        default='full',
        help='CSV format type'
    )
    
    args = parser.parse_args()
    
    generator = EFVIndexGenerator(args.base_dir, args.output_dir)
    
    if args.watch:
        print("👀 Watching for changes...")
        observer = Observer()
        observer.schedule(
            VocabularyWatcher(generator),
            path=str(generator.base_dir),
            recursive=False
        )
        observer.start()
        
        try:
            generator.run()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Stopping watcher...")
            observer.stop()
            observer.join()
    else:
        generator.run()


if __name__ == '__main__':
    main()
