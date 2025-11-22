#!/usr/bin/env python3
"""
Fix grammar typos and remove foreign characters from markdown files.
Preserves all technical terms.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class GrammarFixer:
    def __init__(self, notes_root: str = "notes"):
        self.notes_root = Path(notes_root).resolve()
        self.files_modified = []
        
        # Common grammar typos (non-technical)
        self.grammar_fixes = {
            # Common spelling errors
            'grammer': 'grammar',
            'occured': 'occurred',
            'seperate': 'separate',
            'recieve': 'receive',
            'definately': 'definitely',
            'occurance': 'occurrence',
            'priviledge': 'privilege',
            'priviledges': 'privileges',
            'successfull': 'successful',
            'usefull': 'useful',
            'powerfull': 'powerful',
            'carefull': 'careful',
            'successfuly': 'successfully',
            'succesfully': 'successfully',
            
            # Common grammar errors
            'alot': 'a lot',
            'its own': "its own",  # This is correct, but checking
            
            # Trailing/extra spaces and punctuation
        }
        
        # Foreign/accidental characters to remove
        self.foreign_chars = {
            'ز': '.',  # Arabic character - likely should be period
            '。': '.',  # Chinese/Japanese period
            '、': ',',  # Chinese/Japanese comma
        }
        
    def should_process_file(self, filepath: Path) -> bool:
        """Check if a markdown file should be processed."""
        if filepath.suffix.lower() != '.md':
            return False
        
        # Skip certain directories
        skip_dirs = {'.git', '.obsidian', '.trash', '.makemd', '.space', '.github'}
        try:
            relative_path = filepath.relative_to(self.notes_root.parent)
            parts = relative_path.parts
            if any(part in skip_dirs for part in parts):
                return False
        except ValueError:
            return False
            
        return True
    
    def fix_file(self, filepath: Path) -> Tuple[bool, List[str]]:
        """Fix grammar and foreign characters in a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes = []
            
            # Remove foreign characters
            for foreign, replacement in self.foreign_chars.items():
                if foreign in content:
                    count = content.count(foreign)
                    content = content.replace(foreign, replacement)
                    changes.append(f"Removed '{foreign}' ({count} occurrences)")
            
            # Fix grammar issues (case-sensitive where needed)
            for typo, correct in self.grammar_fixes.items():
                # Word boundary matching to avoid changing parts of technical terms
                # Use case-insensitive matching but preserve original case for first letter
                pattern = r'\b' + re.escape(typo) + r'\b'
                matches = list(re.finditer(pattern, content, re.IGNORECASE))
                
                if matches:
                    for match in reversed(matches):  # Reverse to maintain positions
                        original_word = match.group(0)
                        # Preserve capitalization
                        if original_word[0].isupper():
                            fixed_word = correct.capitalize()
                        else:
                            fixed_word = correct
                        
                        content = content[:match.start()] + fixed_word + content[match.end():]
                    
                    changes.append(f"'{typo}' → '{correct}' ({len(matches)} occurrences)")
            
            # Write back if changed
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, changes
            
            return False, []
            
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            return False, []
    
    def process_all_files(self, dry_run: bool = False):
        """Process all markdown files."""
        markdown_files = []
        for filepath in self.notes_root.rglob("*.md"):
            if self.should_process_file(filepath):
                markdown_files.append(filepath)
        
        print(f"Found {len(markdown_files)} markdown files to check\n")
        
        for filepath in sorted(markdown_files):
            modified, changes = self.fix_file(filepath) if not dry_run else (False, [])
            
            if modified:
                rel_path = filepath.relative_to(self.notes_root)
                print(f"✅ Fixed: {rel_path}")
                for change in changes:
                    print(f"   - {change}")
                self.files_modified.append(filepath)
        
        print(f"\n✨ Complete! Modified {len(self.files_modified)} files")
        if dry_run:
            print("   (Dry run - no files were actually changed)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Fix grammar typos and remove foreign characters'
    )
    parser.add_argument(
        '--notes-root',
        default='notes',
        help='Root directory of notes (default: notes)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    
    args = parser.parse_args()
    
    fixer = GrammarFixer(notes_root=args.notes_root)
    fixer.process_all_files(dry_run=args.dry_run)


if __name__ == '__main__':
    main()
