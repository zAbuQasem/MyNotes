#!/usr/bin/env python3
"""
Remove navigation sections from markdown files.

This script removes the "## Navigation" heading and all content until the next
heading or horizontal rule.
"""

import os
import re
import sys
from pathlib import Path
from typing import List


def remove_navigation_section(content: str) -> tuple[str, bool]:
    """
    Remove navigation section from markdown content.
    
    Returns: (modified_content, was_modified)
    """
    lines = content.split('\n')
    new_lines = []
    in_navigation = False
    modified = False
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is the Navigation heading
        if re.match(r'^##\s+Navigation\s*$', line.strip(), re.IGNORECASE):
            in_navigation = True
            modified = True
            i += 1
            continue
        
        # If we're in navigation section
        if in_navigation:
            # Check if we hit another heading or horizontal rule
            if re.match(r'^#{1,6}\s+', line) or re.match(r'^---+\s*$', line):
                in_navigation = False
                # Don't skip this line, add it
                new_lines.append(line)
            # Skip empty lines and list items in navigation
            elif line.strip() == '' or re.match(r'^\s*[-*]\s+', line):
                pass  # Skip these lines
            else:
                # Something else, end navigation
                in_navigation = False
                new_lines.append(line)
        else:
            new_lines.append(line)
        
        i += 1
    
    # Clean up multiple consecutive empty lines and horizontal rules
    cleaned_lines = []
    prev_empty = False
    prev_hr = False
    
    for line in new_lines:
        is_empty = line.strip() == ''
        is_hr = re.match(r'^---+\s*$', line)
        
        # Skip multiple consecutive empty lines
        if is_empty and prev_empty:
            continue
        
        # Skip multiple consecutive horizontal rules
        if is_hr and prev_hr:
            continue
        
        cleaned_lines.append(line)
        prev_empty = is_empty
        prev_hr = is_hr
    
    return '\n'.join(cleaned_lines), modified


def process_file(filepath: Path, dry_run: bool = False) -> bool:
    """Process a single markdown file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, modified = remove_navigation_section(content)
        
        if modified:
            if not dry_run:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            return True
        
        return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}", file=sys.stderr)
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Remove navigation sections from markdown files'
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
    
    notes_root = Path(args.notes_root)
    if not notes_root.exists():
        print(f"Error: {notes_root} does not exist", file=sys.stderr)
        sys.exit(1)
    
    # Find all markdown files with navigation sections
    files_to_process = []
    for md_file in notes_root.rglob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if re.search(r'^##\s+Navigation\s*$', content, re.MULTILINE | re.IGNORECASE):
                    files_to_process.append(md_file)
        except Exception as e:
            print(f"Error reading {md_file}: {e}", file=sys.stderr)
    
    print(f"Found {len(files_to_process)} files with navigation sections\n")
    
    if not files_to_process:
        print("No files to process!")
        return
    
    modified_count = 0
    for filepath in files_to_process:
        if process_file(filepath, args.dry_run):
            status = "Would remove" if args.dry_run else "Removed"
            print(f"  ✅ {status} navigation from: {filepath.relative_to(notes_root)}")
            modified_count += 1
    
    print(f"\n✨ Complete! {modified_count} files modified")
    if args.dry_run:
        print("   (Dry run - no files were actually changed)")


if __name__ == '__main__':
    main()
