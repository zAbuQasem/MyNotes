#!/usr/bin/env python3
"""
Obsidian to GitBook In-Place Migration Script

Converts Obsidian-style notes to GitBook format IN-PLACE:
- Normalizes filenames to kebab-case (in current directories)
- Flattens single-file folders (except to repo root)
- Rewrites Obsidian wikilinks and image embeds to standard Markdown
- URL-encodes all Markdown link URLs (no spaces)
- Does NOT create SUMMARY.md or new docs/ directory
"""

import argparse
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import quote, unquote


def normalize_filename(name: str) -> str:
    """
    Convert a filename to kebab-case for GitBook.
    - Lowercase letters, digits, and dashes only
    - Convert spaces and underscores to dashes
    - Remove special characters
    - Keep the file extension
    """
    # Split name and extension
    if '.' in name:
        parts = name.rsplit('.', 1)
        stem = parts[0]
        ext = '.' + parts[1]
    else:
        stem = name
        ext = ''
    
    # Convert to lowercase
    stem = stem.lower()
    # Replace spaces and underscores with dashes
    stem = re.sub(r'[\s_]+', '-', stem)
    # Remove special characters except dashes and alphanumerics
    stem = re.sub(r'[^a-z0-9-]', '', stem)
    # Remove multiple consecutive dashes
    stem = re.sub(r'-+', '-', stem)
    # Strip leading/trailing dashes
    stem = stem.strip('-')
    
    return stem + ext


def url_encode_path(path: str) -> str:
    """
    URL-encode a relative path, preserving forward slashes.
    Spaces become %20, etc.
    """
    # Split by / to preserve directory separators
    parts = path.split('/')
    # Quote each part (spaces -> %20, etc), but keep forward slashes
    encoded_parts = [quote(part) for part in parts]
    return '/'.join(encoded_parts)


def is_ignored_dir(path: Path, ignore_dirs: List[str]) -> bool:
    """Check if path contains any ignored directory."""
    parts = path.parts
    return any(ignored in parts for ignored in ignore_dirs)


def is_image_file(path: str) -> bool:
    """Check if the path is an image file."""
    image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp', '.bmp'}
    return Path(path).suffix.lower() in image_extensions


def find_all_notes(notes_root: Path, ignore_dirs: List[str]) -> List[Path]:
    """Find all markdown files in notes_root, excluding ignored directories."""
    notes = []
    for md_file in notes_root.rglob('*.md'):
        rel_path = md_file.relative_to(notes_root)
        if not is_ignored_dir(rel_path, ignore_dirs):
            notes.append(md_file)
    return notes


def find_single_file_folders(notes_root: Path, ignore_dirs: List[str]) -> List[Path]:
    """
    Find all directories that contain exactly one file and no subdirectories.
    Exclude directories whose parent is the repo root.
    """
    single_file_folders = []
    
    for dirpath, dirnames, filenames in os.walk(notes_root):
        dir_path = Path(dirpath)
        rel_path = dir_path.relative_to(notes_root)
        
        # Skip ignored directories
        if is_ignored_dir(rel_path, ignore_dirs):
            continue
        
        # Skip root directory
        if dir_path == notes_root:
            continue
        
        # Check if this directory has exactly 1 file and 0 subdirectories
        if len(filenames) == 1 and len(dirnames) == 0:
            # Check if parent is repo root - if so, don't flatten
            parent = dir_path.parent
            if parent != notes_root:
                single_file_folders.append(dir_path)
    
    return single_file_folders


def flatten_single_file_folders(
    single_file_folders: List[Path],
    notes_root: Path,
    dry_run: bool = False
) -> Dict[Path, Path]:
    """
    Flatten single-file folders by moving the file up one level.
    Returns a mapping of old_path -> new_path for all moved files.
    """
    moved_files = {}
    
    for folder in single_file_folders:
        # Get the single file in this folder
        files = list(folder.iterdir())
        if len(files) != 1:
            continue
        
        file_path = files[0]
        if not file_path.is_file():
            continue
        
        # New location is parent directory
        new_path = folder.parent / file_path.name
        
        if dry_run:
            print(f"  [DRY-RUN] Would move: {file_path.relative_to(notes_root)} -> {new_path.relative_to(notes_root)}")
        else:
            # Move the file
            shutil.move(str(file_path), str(new_path))
            print(f"  Moved: {file_path.relative_to(notes_root)} -> {new_path.relative_to(notes_root)}")
            
            # Try to remove the now-empty directory
            try:
                folder.rmdir()
            except OSError:
                pass  # Directory not empty or other issue
        
        moved_files[file_path] = new_path
    
    return moved_files


def normalize_filenames(
    notes: List[Path],
    notes_root: Path,
    dry_run: bool = False
) -> Dict[Path, Path]:
    """
    Normalize all markdown filenames to kebab-case in their current directories.
    Returns a mapping of old_path -> new_path for all renamed files.
    """
    renamed_files = {}
    
    for note_path in notes:
        old_name = note_path.name
        
        # Skip SUMMARY.md - it should never be renamed or modified
        if old_name.upper() == 'SUMMARY.MD':
            continue
        
        new_name = normalize_filename(old_name)
        
        if old_name != new_name:
            new_path = note_path.parent / new_name
            
            if dry_run:
                print(f"  [DRY-RUN] Would rename: {note_path.relative_to(notes_root)} -> {new_path.relative_to(notes_root)}")
            else:
                # Check if target already exists
                if new_path.exists() and new_path != note_path:
                    print(f"  WARNING: Target exists, skipping: {new_path.relative_to(notes_root)}")
                    continue
                
                note_path.rename(new_path)
                print(f"  Renamed: {note_path.relative_to(notes_root)} -> {new_path.relative_to(notes_root)}")
            
            renamed_files[note_path] = new_path
    
    return renamed_files


def build_note_mapping(notes_root: Path, ignore_dirs: List[str]) -> Dict[str, Path]:
    """
    Build a mapping from note stem (lowercase, case-insensitive) to absolute path.
    This is used to resolve wikilinks.
    """
    mapping = {}
    notes = find_all_notes(notes_root, ignore_dirs)
    
    for note_path in notes:
        key = note_path.stem.lower()
        # Handle duplicates by keeping the first one found
        if key not in mapping:
            mapping[key] = note_path
    
    return mapping


def compute_relative_path(from_path: Path, to_path: Path) -> str:
    """
    Compute relative path from from_path to to_path.
    Both paths should be absolute.
    """
    try:
        # Get parent directory of from_path (the directory containing the file)
        from_dir = from_path.parent
        # Compute relative path
        rel_path = os.path.relpath(to_path, from_dir)
        return rel_path.replace('\\', '/')
    except ValueError:
        # Different drives on Windows, return absolute-ish path
        return str(to_path).replace('\\', '/')


def resolve_wikilink_target(
    link_text: str,
    note_mapping: Dict[str, Path]
) -> Optional[Path]:
    """
    Resolve a wikilink target to its absolute path.
    Returns None if not found.
    """
    # Extract the note name (before any | alias)
    note_name = link_text.split('|')[0].strip()
    
    # Handle section links (e.g., "Note#Section")
    if '#' in note_name:
        note_name = note_name.split('#')[0].strip()
    
    # Normalize: lowercase and replace spaces with dashes
    key = note_name.lower().replace(' ', '-')
    result = note_mapping.get(key)
    
    # If not found, try stripping numeric prefixes (e.g., "4-domain-persistence" -> "domain-persistence")
    if result is None and re.match(r'^\d+-', key):
        key_without_prefix = re.sub(r'^\d+-', '', key)
        result = note_mapping.get(key_without_prefix)
    
    return result


def rewrite_wikilinks(
    content: str,
    current_note_path: Path,
    note_mapping: Dict[str, Path],
    notes_root: Path
) -> str:
    """
    Rewrite Obsidian wikilinks to standard Markdown.
    Handles both note links and image embeds.
    """
    # Pattern for wikilinks: [[target]] or [[target|alias]]
    # And image embeds: ![[image.png]] or ![[image.png|alt]]
    pattern = r'(!?)\[\[([^\]]+)\]\]'
    
    def replace_wikilink(match):
        is_embed = match.group(1) == '!'
        link_content = match.group(2)
        
        # Parse target and alias/alt text
        if '|' in link_content:
            target, alias = link_content.split('|', 1)
            target = target.strip()
            alias = alias.strip()
        else:
            target = link_content.strip()
            alias = None
        
        # Check if target is an image
        if is_image_file(target):
            # It's an image embed
            # Resolve image relative to current note location
            current_note_dir = current_note_path.parent
            
            # Try to find the image in multiple locations
            image_path = current_note_dir / target
            
            # If not found, try common locations
            if not image_path.exists():
                # Try attachments subfolder in current directory
                attachments_path = current_note_dir / 'attachments' / Path(target).name
                if attachments_path.exists():
                    image_path = attachments_path
                else:
                    # Try parent directory's attachments subfolder
                    parent_attachments = current_note_dir.parent / 'attachments' / Path(target).name
                    if parent_attachments.exists():
                        image_path = parent_attachments
                    else:
                        # Try Assets subfolder
                        assets_path = current_note_dir / 'Assets' / Path(target).name
                        if assets_path.exists():
                            image_path = assets_path
                        else:
                            # Try parent's Assets subfolder
                            parent_assets = current_note_dir.parent / 'Assets' / Path(target).name
                            if parent_assets.exists():
                                image_path = parent_assets
            
            # Compute relative path
            if image_path.exists():
                rel_path = compute_relative_path(current_note_path, image_path)
                rel_path_encoded = url_encode_path(rel_path)
                alt_text = alias if alias else Path(target).stem
                return f'![{alt_text}]({rel_path_encoded})'
            else:
                # Image not found, keep original
                print(f"  WARNING: Image not found: {target} (from {current_note_path.name})")
                return match.group(0)
        else:
            # It's a note link
            target_path = resolve_wikilink_target(target, note_mapping)
            if target_path:
                # Compute relative path
                rel_path = compute_relative_path(current_note_path, target_path)
                rel_path_encoded = url_encode_path(rel_path)
                
                # Preserve section links
                section = ''
                if '#' in link_content.split('|')[0]:
                    section_part = link_content.split('|')[0].split('#', 1)[1]
                    # Normalize the fragment ID to GitBook/GitHub format
                    section = '#' + normalize_fragment_id(section_part)
                
                link_text = alias if alias else Path(target).stem
                return f'[{link_text}]({rel_path_encoded}{section})'
            else:
                # Keep original if not found
                print(f"  WARNING: Could not resolve wikilink: [[{link_content}]] (from {current_note_path.name})")
                return match.group(0)
    
    return re.sub(pattern, replace_wikilink, content)


def normalize_fragment_id(heading: str) -> str:
    """
    Normalize a heading text to a GitHub/GitBook-compatible fragment ID.
    - Convert to lowercase
    - Replace spaces with dashes
    - Remove special characters except dashes
    - Remove leading/trailing dashes
    """
    # Convert to lowercase
    fragment = heading.lower()
    # Replace spaces and underscores with dashes
    fragment = re.sub(r'[\s_]+', '-', fragment)
    # Remove special characters except dashes and alphanumerics
    fragment = re.sub(r'[^a-z0-9-]', '', fragment)
    # Remove multiple consecutive dashes
    fragment = re.sub(r'-+', '-', fragment)
    # Strip leading/trailing dashes
    fragment = fragment.strip('-')
    return fragment


def rewrite_fragment_links(content: str) -> str:
    """
    Rewrite fragment links (heading anchors) to use proper GitBook/GitHub format.
    Converts links like #Symbols%20and%20stripped%20binaries to #symbols-and-stripped-binaries
    """
    # Pattern for fragment links: [text](#fragment)
    pattern = r'\[([^\]]+)\]\(#([^)]+)\)'
    
    def replace_fragment(match):
        text = match.group(1)
        fragment = match.group(2)
        
        # Decode URL-encoded characters (e.g., %20 -> space)
        fragment_decoded = unquote(fragment)
        
        # Normalize the fragment ID
        fragment_normalized = normalize_fragment_id(fragment_decoded)
        
        return f'[{text}](#{fragment_normalized})'
    
    return re.sub(pattern, replace_fragment, content)


def rewrite_markdown_links(
    content: str,
    current_note_path: Path
) -> str:
    """
    Rewrite standard Markdown links to ensure URLs are URL-encoded.
    Handles both image and regular links.
    """
    # Pattern for Markdown links: [text](url) or ![alt](url)
    pattern = r'(!?)\[([^\]]*)\]\(([^)]+)\)'
    
    def replace_link(match):
        is_image = match.group(1) == '!'
        text = match.group(2)
        url = match.group(3)
        
        # Skip absolute URLs and fragment-only links (handled by rewrite_fragment_links)
        if url.startswith('http://') or url.startswith('https://') or url.startswith('#'):
            return match.group(0)
        
        # Decode URL-encoded characters first
        url_decoded = unquote(url)
        
        # Check if path has spaces or needs encoding
        url_encoded = url_encode_path(url_decoded)
        if ' ' in url_decoded or url != url_encoded:
            # Re-encode properly
            prefix = '!' if is_image else ''
            return f'{prefix}[{text}]({url_encoded})'
        
        return match.group(0)
    
    return re.sub(pattern, replace_link, content)


def rewrite_note_content(
    note_path: Path,
    note_mapping: Dict[str, Path],
    notes_root: Path,
    dry_run: bool = False
) -> bool:
    """
    Rewrite the content of a note to convert Obsidian links to standard Markdown.
    Returns True if changes were made.
    """
    try:
        with open(note_path, 'r', encoding='utf-8') as f:
            original_content = f.read()
    except Exception as e:
        print(f"  ERROR reading {note_path}: {e}")
        return False
    
    # Rewrite wikilinks
    content = rewrite_wikilinks(original_content, note_path, note_mapping, notes_root)
    
    # Rewrite fragment links (heading anchors)
    content = rewrite_fragment_links(content)
    
    # Rewrite standard Markdown links
    content = rewrite_markdown_links(content, note_path)
    
    # Check if content changed
    if content != original_content:
        if dry_run:
            print(f"  [DRY-RUN] Would update content: {note_path.relative_to(notes_root)}")
        else:
            with open(note_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Updated content: {note_path.relative_to(notes_root)}")
        return True
    
    return False


def main():
    parser = argparse.ArgumentParser(
        description='Migrate Obsidian notes to GitBook format IN-PLACE'
    )
    parser.add_argument(
        '--notes-root',
        type=str,
        default='.',
        help='Root directory of Obsidian notes (default: current directory)'
    )
    parser.add_argument(
        '--ignore-dir',
        action='append',
        default=[],
        help='Directories to ignore (can be specified multiple times)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without writing'
    )
    
    args = parser.parse_args()
    
    # Set default ignore directories
    if not args.ignore_dir:
        args.ignore_dir = ['.git', '.obsidian', '.trash', '.makemd', '.space', '.github', 'scripts']
    
    # Convert to absolute paths
    notes_root = Path(args.notes_root).resolve()
    
    print("=" * 70)
    print("Obsidian → GitBook In-Place Migration")
    print("=" * 70)
    print(f"Notes root: {notes_root}")
    print(f"Ignoring: {', '.join(args.ignore_dir)}")
    if args.dry_run:
        print("DRY RUN MODE - No changes will be made")
    print()
    
    # PHASE A: SCAN
    print("PHASE A: Scanning repository...")
    print("-" * 70)
    all_notes = find_all_notes(notes_root, args.ignore_dir)
    single_file_folders = find_single_file_folders(notes_root, args.ignore_dir)
    
    print(f"Found {len(all_notes)} markdown notes")
    print(f"Found {len(single_file_folders)} single-file folders to flatten")
    print()
    
    if not all_notes:
        print("No notes found to migrate.")
        return
    
    # PHASE B: FLATTEN SINGLE-FILE FOLDERS
    print("PHASE B: Flattening single-file folders...")
    print("-" * 70)
    if single_file_folders:
        moved_files = flatten_single_file_folders(single_file_folders, notes_root, args.dry_run)
        print(f"Flattened {len(moved_files)} folders")
    else:
        print("No single-file folders to flatten")
        moved_files = {}
    print()
    
    # Refresh notes list after flattening
    if not args.dry_run and moved_files:
        all_notes = find_all_notes(notes_root, args.ignore_dir)
    
    # PHASE C: NORMALIZE FILENAMES
    print("PHASE C: Normalizing filenames to kebab-case...")
    print("-" * 70)
    renamed_files = normalize_filenames(all_notes, notes_root, args.dry_run)
    print(f"Normalized {len(renamed_files)} filenames")
    print()
    
    # Refresh notes list after renaming
    if not args.dry_run and renamed_files:
        all_notes = find_all_notes(notes_root, args.ignore_dir)
    
    # PHASE D: REWRITE CONTENT
    print("PHASE D: Rewriting content (wikilinks, URLs, encoding)...")
    print("-" * 70)
    
    # Build note mapping for link resolution
    note_mapping = build_note_mapping(notes_root, args.ignore_dir)
    print(f"Built note mapping with {len(note_mapping)} entries")
    
    # Process each note's content
    updated_count = 0
    for note_path in all_notes:
        changed = rewrite_note_content(note_path, note_mapping, notes_root, args.dry_run)
        if changed:
            updated_count += 1
    
    print(f"Updated content in {updated_count} notes")
    print()
    
    # SUMMARY
    print("=" * 70)
    print("Migration Summary")
    print("=" * 70)
    print(f"  Folders flattened: {len(moved_files)}")
    print(f"  Files renamed: {len(renamed_files)}")
    print(f"  Content updated: {updated_count}")
    print()
    
    if args.dry_run:
        print("DRY RUN complete - no changes were made")
        print("Run without --dry-run to apply changes")
    else:
        print("Migration complete!")
        print()
        print("IMPORTANT: This migration is IN-PLACE")
        print("  - No SUMMARY.md was created")
        print("  - No new docs/ directory was created")
        print("  - All changes are in existing folder structure")


if __name__ == '__main__':
    main()
