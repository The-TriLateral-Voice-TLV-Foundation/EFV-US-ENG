#!/usr/bin/env python3
"""
🔍 EFV Diagnostic Script
Finds mismatches between indices and actual JSON files
"""

import json
import os
from pathlib import Path
from collections import defaultdict

def diagnose_efv():
    # Find vocab directory
    possible_paths = [
        Path.home() / "Desktop/code/src/github/TLV-Foundation/efv-us-eng/vocab",
        Path("/home/devuser/Desktop/code/src/github/TLV-Foundation/efv-us-eng/vocab"),
        Path("./vocab"),
        Path("../vocab"),
    ]
    
    vocab_dir = None
    for p in possible_paths:
        if p.exists():
            vocab_dir = p
            break
    
    if not vocab_dir:
        print("❌ Could not find vocab directory")
        return
    
    print(f"📂 Using vocab directory: {vocab_dir}\n")
    
    # Load all indices
    indices_dir = vocab_dir / "_indices"
    all_indexed_words = set()
    
    if indices_dir.exists():
        print("📋 Loading indices...")
        for idx_file in indices_dir.glob("*_index.json"):
            with open(idx_file) as f:
                index_data = json.load(f)
                all_indexed_words.update(index_data.keys())
        print(f"  ✓ Found {len(all_indexed_words)} indexed words\n")
    
    # Check each letter file
    print("🔎 Checking letter files vs indices...\n")
    
    mismatches = defaultdict(list)
    file_counts = {}
    
    for letter_file in sorted(vocab_dir.glob("*.json")):
        if letter_file.name.startswith("_"):
            continue
        
        letter = letter_file.stem.upper()
        
        with open(letter_file) as f:
            file_data = json.load(f)
        
        file_words = set(file_data.keys())
        file_counts[letter] = len(file_words)
        
        # Words in index but not in file
        indexed_for_letter = {w for w in all_indexed_words if w[0] == letter}
        missing_from_file = indexed_for_letter - file_words
        
        if missing_from_file:
            mismatches[letter] = sorted(missing_from_file)
    
    # Report
    print("📊 Words per letter file:")
    for letter in sorted(file_counts.keys()):
        count = file_counts[letter]
        status = "✓" if count > 0 else "❌"
        print(f"  {status} {letter}.json: {count} words")
    
    if mismatches:
        print("\n⚠️  MISMATCHES FOUND:\n")
        for letter in sorted(mismatches.keys()):
            words = mismatches[letter]
            print(f"  Letter {letter}:")
            print(f"    Indexed but missing from {letter}.json: {len(words)} words")
            if len(words) <= 5:
                for w in words[:5]:
                    print(f"      - {w}")
            else:
                for w in words[:3]:
                    print(f"      - {w}")
                print(f"      ... and {len(words) - 3} more")
    
    # Check for children arrays
    print("\n🏗️  Checking for children arrays...\n")
    
    sample_file = vocab_dir / "p.json"
    if sample_file.exists():
        with open(sample_file) as f:
            data = json.load(f)
        
        first_word = list(data.keys())[0] if data else None
        if first_word:
            word_obj = data[first_word]
            has_children = "children" in word_obj
            
            if has_children:
                children_count = len(word_obj.get("children", []))
                print(f"  ✓ Sample word has {children_count} children sections")
            else:
                print(f"  ❌ Sample word ({first_word}) has NO children array")
                print(f"     Available keys: {list(word_obj.keys())}")
    
    print("\n" + "="*60)
    print("💡 Next Steps:")
    if mismatches:
        print("  1. Run: python rebuild-indices.py")
        print("     (This will rebuild indices to match actual files)")
    if not any("children" in v for file_data in [json.load(open(f)) for f in vocab_dir.glob("*.json") if not f.name.startswith("_")] for v in file_data.values()):
        print("  2. Run: python populate-sections.py")
        print("     (This will add 7-section children arrays to all words)")
    print("="*60)

if __name__ == "__main__":
    diagnose_efv()
