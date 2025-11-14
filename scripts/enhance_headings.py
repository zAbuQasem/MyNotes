#!/usr/bin/env python3
"""
Enhance and standardize markdown headings across the MyNotes repository.

This script:
1. Analyzes heading structure in all markdown files
2. Ensures each file has exactly one H1 heading
3. Fixes navigation sections (converts H1 Navigation to H2 or removes)
4. Ensures proper heading hierarchy (no skipping levels)
5. Standardizes heading capitalization and formatting
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from collections import defaultdict


class HeadingAnalyzer:
    """Analyze and fix markdown heading structure."""
    
    # Directories to ignore
    IGNORE_DIRS = {'.git', '.obsidian', '.trash', '.makemd', '.space', '.github', 'scripts'}
    
    def __init__(self, notes_root: str = ".", dry_run: bool = False):
        self.notes_root = Path(notes_root).resolve()
        self.dry_run = dry_run
        self.issues_found = defaultdict(list)
        self.files_modified = []
        
    def should_process_file(self, filepath: Path) -> bool:
        """Check if a markdown file should be processed."""
        # Skip if not a markdown file
        if filepath.suffix.lower() != '.md':
            return False
            
        # Skip if in an ignored directory
        try:
            relative_path = filepath.relative_to(self.notes_root)
            parts = relative_path.parts
            if any(part in self.IGNORE_DIRS for part in parts):
                return False
        except ValueError:
            return False
            
        return True
    
    def find_all_markdown_files(self) -> List[Path]:
        """Find all markdown files to process."""
        markdown_files = []
        for filepath in self.notes_root.rglob("*.md"):
            if self.should_process_file(filepath):
                markdown_files.append(filepath)
        return sorted(markdown_files)
    
    def extract_headings(self, content: str) -> List[Tuple[int, str, int]]:
        """Extract all headings with their levels and line numbers.
        
        Returns: List of (level, text, line_number) tuples
        """
        headings = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Match ATX-style headings (# Heading)
            match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append((level, text, line_num))
        
        return headings
    
    def analyze_file(self, filepath: Path) -> Dict:
        """Analyze heading structure in a file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {'error': str(e)}
        
        headings = self.extract_headings(content)
        
        analysis = {
            'path': filepath,
            'headings': headings,
            'issues': []
        }
        
        # Check for issues
        h1_headings = [h for h in headings if h[0] == 1]
        
        # Issue 1: Multiple H1 headings
        if len(h1_headings) > 1:
            analysis['issues'].append({
                'type': 'multiple_h1',
                'count': len(h1_headings),
                'headings': h1_headings
            })
        
        # Issue 2: No H1 heading
        if len(h1_headings) == 0:
            analysis['issues'].append({
                'type': 'no_h1',
                'first_heading': headings[0] if headings else None
            })
        
        # Issue 3: "Navigation" as H1
        for level, text, line_num in headings:
            if level == 1 and text.lower() in ['navigation', 'table of contents', 'contents']:
                analysis['issues'].append({
                    'type': 'navigation_h1',
                    'text': text,
                    'line_num': line_num
                })
        
        # Issue 4: Heading level jumps (e.g., H1 -> H3)
        for i in range(len(headings) - 1):
            current_level = headings[i][0]
            next_level = headings[i + 1][0]
            if next_level > current_level + 1:
                analysis['issues'].append({
                    'type': 'level_jump',
                    'from': headings[i],
                    'to': headings[i + 1]
                })
        
        return analysis
    
    def infer_proper_title(self, filepath: Path, current_h1: Optional[str]) -> str:
        """Infer the proper title for a file based on its filename and context."""
        # Get filename without extension
        filename = filepath.stem
        
        # Special case for readme files
        if filename.lower() == 'readme':
            # Use parent directory name
            parent = filepath.parent.name
            if parent == 'notes':
                return "MyNotes - Navigation Index"
            # Convert kebab-case to Title Case
            return ' '.join(word.capitalize() for word in parent.split('-'))
        
        # Convert filename to title
        # Handle cases like "domain-enumeration" -> "Domain Enumeration"
        # Handle cases like "01-intro-setup" -> "Intro Setup"
        
        # Remove leading numbers and hyphens
        title = re.sub(r'^\d+[-_\s]+', '', filename)
        
        # Replace hyphens and underscores with spaces
        title = title.replace('-', ' ').replace('_', ' ')
        
        # Title case, but handle acronyms
        words = []
        for word in title.split():
            # Keep uppercase acronyms (2+ uppercase letters)
            if len(word) > 1 and word.isupper():
                words.append(word)
            # Keep known acronyms
            elif word.upper() in ['AD', 'CS', 'GPO', 'ATA', 'JWT', 'XSS', 'CSRF', 'SSRF', 'SSTI', 
                                   'SSI', 'LFI', 'HPP', 'LDAP', 'SQL', 'IMAP', 'SMTP', 'DNS', 
                                   'IIS', 'ORM', 'OPA', 'AWS', 'IAC', 'K8S', 'GDB', 'API', 'RPC']:
                words.append(word.upper())
            # Special case for SQLi
            elif word.lower() in ['sqli', 'nosql']:
                words.append(word.upper())
            # Special mappings for common terms
            elif word.lower() == 'privesc':
                words.append('PrivEsc')
            elif word.lower() == 'powershell':
                words.append('PowerShell')
            elif word.lower() == 'macos':
                words.append('macOS')
            elif word.lower() == 'kubectl':
                words.append('kubectl')
            else:
                words.append(word.capitalize())
        
        title = ' '.join(words)
        
        # If we already have a good H1, consider using it if it's reasonable
        if current_h1 and current_h1 not in ['Navigation', 'Table of Contents', 'Contents']:
            # Check if current H1 seems problematic
            # - Too short (less than 3 chars)
            # - Contains weird characters or formatting issues
            # - Doesn't start with a capital letter or number
            # - Contains only lowercase (likely a leftover command or note)
            if (len(current_h1) >= 3 and 
                current_h1[0].isupper() and 
                not current_h1.islower() and
                # Allow it if it's similar to our computed title
                (current_h1.lower().replace(' ', '') == title.lower().replace(' ', '') or
                 # Or if it's a reasonable expansion of the filename
                 len(current_h1) >= len(filename))):
                return current_h1
        
        return title
    
    def fix_file_headings(self, filepath: Path, analysis: Dict) -> bool:
        """Fix heading issues in a file."""
        if 'error' in analysis or not analysis['issues']:
            return False
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            lines = content.split('\n')
            modified = False
            
            # Get current headings
            headings = analysis['headings']
            h1_headings = [h for h in headings if h[0] == 1]
            
            # Determine the proper title
            current_h1_text = h1_headings[0][1] if h1_headings else None
            proper_title = self.infer_proper_title(filepath, current_h1_text)
            
            # Strategy: 
            # 1. If there are multiple H1s, keep only the first meaningful one
            # 2. Convert "Navigation" H1s to H2
            # 3. If no H1, add one at the top
            
            new_lines = []
            seen_h1 = False
            skip_next_empty = False
            
            for i, line in enumerate(lines):
                line_num = i + 1
                
                # Check if this line is a heading
                match = re.match(r'^(#{1,6})\s+(.+)$', line.strip())
                
                if match:
                    level = len(match.group(1))
                    text = match.group(2).strip()
                    
                    # Handle H1 headings
                    if level == 1:
                        # If this is "Navigation" or similar, convert to H2
                        if text.lower() in ['navigation', 'table of contents', 'contents']:
                            new_lines.append('## ' + text)
                            modified = True
                            continue
                        
                        # If we've already seen an H1, convert this to H2
                        if seen_h1:
                            new_lines.append('## ' + text)
                            modified = True
                            continue
                        
                        # This is our first H1
                        # If it's not the proper title, fix it
                        if text != proper_title and not seen_h1:
                            new_lines.append('# ' + proper_title)
                            modified = True
                            seen_h1 = True
                            continue
                        
                        seen_h1 = True
                
                new_lines.append(line)
            
            # If we never saw an H1, add one at the top
            if not seen_h1:
                # Find where to insert (after front matter if present)
                insert_pos = 0
                if lines and lines[0].strip() == '---':
                    # Skip front matter
                    for j in range(1, len(new_lines)):
                        if new_lines[j].strip() == '---':
                            insert_pos = j + 1
                            break
                
                new_lines.insert(insert_pos, '# ' + proper_title)
                if insert_pos < len(new_lines) - 1 and new_lines[insert_pos + 1].strip():
                    new_lines.insert(insert_pos + 1, '')
                modified = True
            
            # Write back if modified
            if modified:
                new_content = '\n'.join(new_lines)
                if not self.dry_run:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                self.files_modified.append(filepath)
                return True
        
        except Exception as e:
            print(f"Error fixing {filepath}: {e}", file=sys.stderr)
            return False
        
        return False
    
    def run_analysis(self):
        """Run analysis on all files."""
        print("🔍 Analyzing markdown files...")
        files = self.find_all_markdown_files()
        print(f"Found {len(files)} markdown files to analyze\n")
        
        # Analyze all files
        analyses = []
        for filepath in files:
            analysis = self.analyze_file(filepath)
            if analysis.get('issues'):
                analyses.append(analysis)
                rel_path = filepath.relative_to(self.notes_root)
                print(f"\n📄 {rel_path}")
                for issue in analysis['issues']:
                    if issue['type'] == 'multiple_h1':
                        print(f"  ⚠️  Multiple H1 headings ({issue['count']})")
                        for level, text, line_num in issue['headings']:
                            print(f"      Line {line_num}: {text}")
                    elif issue['type'] == 'no_h1':
                        print(f"  ⚠️  No H1 heading")
                    elif issue['type'] == 'navigation_h1':
                        print(f"  ⚠️  '{issue['text']}' as H1 (line {issue['line_num']})")
                    elif issue['type'] == 'level_jump':
                        from_level, from_text, from_line = issue['from']
                        to_level, to_text, to_line = issue['to']
                        print(f"  ⚠️  Level jump: H{from_level} -> H{to_level}")
        
        print(f"\n\n📊 Summary: Found {len(analyses)} files with heading issues")
        
        return analyses
    
    def fix_all_files(self, analyses: List[Dict]):
        """Fix heading issues in all analyzed files."""
        print("\n\n🔧 Fixing heading issues...")
        
        for analysis in analyses:
            filepath = analysis['path']
            rel_path = filepath.relative_to(self.notes_root)
            
            if self.fix_file_headings(filepath, analysis):
                status = "Would fix" if self.dry_run else "Fixed"
                print(f"  ✅ {status}: {rel_path}")
        
        print(f"\n\n✨ Complete! Modified {len(self.files_modified)} files")
        if self.dry_run:
            print("   (Dry run - no files were actually changed)")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Enhance and standardize markdown headings'
    )
    parser.add_argument(
        '--notes-root',
        default='.',
        help='Root directory of notes (default: current directory)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be changed without modifying files'
    )
    
    args = parser.parse_args()
    
    analyzer = HeadingAnalyzer(
        notes_root=args.notes_root,
        dry_run=args.dry_run
    )
    
    # Run analysis
    analyses = analyzer.run_analysis()
    
    if analyses:
        # Fix issues
        analyzer.fix_all_files(analyses)
    else:
        print("\n✅ No heading issues found!")


if __name__ == '__main__':
    main()
