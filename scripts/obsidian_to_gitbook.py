#!/usr/bin/env python3
"""
Obsidian to GitBook Migration Script

Converts Obsidian-style notes to GitBook format:
- Normalizes filenames and paths to kebab-case
- Rewrites Obsidian wikilinks and image embeds
- Rewrites standard Markdown image links
- Copies and organizes images to docs/assets/
- Creates docs/index.md from root README.md
"""

import argparse
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from urllib.parse import unquote


def normalize_path_component(name: str) -> str:
    """
    Convert a path component to kebab-case.
    - Lowercase letters, digits, and dashes only
    - Convert spaces and underscores to dashes
    - Remove special characters
    """
    # Convert to lowercase
    name = name.lower()
    # Replace spaces and underscores with dashes
    name = re.sub(r'[\s_]+', '-', name)
    # Remove special characters except dashes and alphanumerics
    name = re.sub(r'[^a-z0-9-]', '', name)
    # Remove multiple consecutive dashes
    name = re.sub(r'-+', '-', name)
    # Strip leading/trailing dashes
    name = name.strip('-')
    return name


def normalize_path(path: Path, base_path: Path) -> Path:
    """
    Normalize a full path to kebab-case.
    Returns the path relative to base_path with normalized components.
    """
    rel_path = path.relative_to(base_path)
    parts = list(rel_path.parts)
    
    # Normalize directory components
    normalized_parts = []
    for i, part in enumerate(parts):
        if i == len(parts) - 1 and part.endswith('.md'):
            # For the file, normalize the stem and keep .md
            stem = part[:-3]
            normalized_parts.append(normalize_path_component(stem) + '.md')
        else:
            # For directories
            normalized_parts.append(normalize_path_component(part))
    
    return Path(*normalized_parts) if normalized_parts else Path('.')


def get_note_key(path: Path) -> str:
    """Get the note key (lowercased stem) for mapping."""
    return path.stem.lower()


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
        if not is_ignored_dir(md_file.relative_to(notes_root), ignore_dirs):
            notes.append(md_file)
    return notes


def build_note_mapping(notes: List[Path], notes_root: Path, docs_dir: Path) -> Dict[str, Path]:
    """
    Build a mapping from note key (lowercased stem) to new docs path.
    """
    mapping = {}
    for note_path in notes:
        key = get_note_key(note_path)
        new_path = docs_dir / normalize_path(note_path, notes_root)
        mapping[key] = new_path
    return mapping


def resolve_wikilink_target(link_text: str, note_mapping: Dict[str, Path]) -> Optional[Path]:
    """
    Resolve a wikilink target to its new path.
    Returns None if not found.
    """
    # Extract the note name (before any | alias)
    note_name = link_text.split('|')[0].strip()
    key = note_name.lower()
    return note_mapping.get(key)


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


def copy_image_to_assets(
    image_src: Path,
    original_note_path: Path,
    notes_root: Path,
    assets_dir: Path,
    copied_images: Set[str]
) -> Path:
    """
    Copy an image to the assets directory, preserving some structure.
    Returns the new path relative to notes_root.
    """
    # Create a unique path based on the original note's location
    # to avoid naming conflicts
    rel_note_path = original_note_path.relative_to(notes_root)
    note_dir = rel_note_path.parent
    
    # Build target path: docs/assets/<note_dir>/<image_name>
    target_rel_path = note_dir / image_src.name
    target_path = assets_dir / target_rel_path
    
    # Create target directory
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy if not already copied
    src_str = str(image_src.resolve())
    if src_str not in copied_images:
        if image_src.exists():
            shutil.copy2(image_src, target_path)
            copied_images.add(src_str)
        else:
            print(f"Warning: Image not found: {image_src}")
    
    return target_path


def rewrite_wikilinks(
    content: str,
    current_note_path: Path,
    original_note_path: Path,
    notes_root: Path,
    docs_dir: Path,
    assets_dir: Path,
    note_mapping: Dict[str, Path],
    copied_images: Set[str]
) -> str:
    """
    Rewrite Obsidian wikilinks in the content.
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
            alias = target
        
        # Check if it's an image
        if is_image_file(target):
            # It's an image embed
            # Resolve image relative to original note location
            original_note_dir = original_note_path.parent
            image_src = original_note_dir / target
            
            # Copy to assets
            target_path = copy_image_to_assets(
                image_src, original_note_path, notes_root, assets_dir, copied_images
            )
            
            # Compute relative path from new note location to asset
            rel_path = compute_relative_path(current_note_path, target_path)
            
            # Return Markdown image syntax
            return f'![{alias}]({rel_path})'
        else:
            # It's a note link
            target_path = resolve_wikilink_target(target, note_mapping)
            if target_path:
                # Compute relative path
                rel_path = compute_relative_path(current_note_path, target_path)
                return f'[{alias}]({rel_path})'
            else:
                # Keep original if not found
                print(f"Warning: Could not resolve wikilink: [[{link_content}]]")
                return match.group(0)
    
    return re.sub(pattern, replace_wikilink, content)


def rewrite_markdown_images(
    content: str,
    current_note_path: Path,
    original_note_path: Path,
    notes_root: Path,
    docs_dir: Path,
    assets_dir: Path,
    copied_images: Set[str]
) -> str:
    """
    Rewrite standard Markdown image links to use docs/assets/.
    Only handles relative (local) image paths.
    """
    # Pattern for Markdown images: ![alt](path)
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    def replace_image(match):
        alt_text = match.group(1)
        image_path = match.group(2)
        
        # Skip absolute URLs
        if image_path.startswith('http://') or image_path.startswith('https://'):
            return match.group(0)
        
        # Decode URL-encoded characters (e.g., %20 -> space)
        image_path = unquote(image_path)
        
        # Skip if it's not an image
        if not is_image_file(image_path):
            return match.group(0)
        
        # Resolve relative to original note location
        original_note_dir = original_note_path.parent
        image_src = original_note_dir / image_path
        
        # If the image doesn't exist, try common Obsidian locations
        if not image_src.exists():
            # Try Assets subdirectory
            assets_subdir = original_note_dir / 'Assets'
            if assets_subdir.exists():
                alt_src = assets_subdir / Path(image_path).name
                if alt_src.exists():
                    image_src = alt_src
            
            # Try attachments subdirectory
            if not image_src.exists():
                attachments_subdir = original_note_dir / 'attachments'
                if attachments_subdir.exists():
                    alt_src = attachments_subdir / Path(image_path).name
                    if alt_src.exists():
                        image_src = alt_src
        
        # Try to normalize the path
        try:
            image_src = image_src.resolve()
        except Exception:
            # If resolution fails, keep original
            return match.group(0)
        
        # Copy to assets
        target_path = copy_image_to_assets(
            image_src, original_note_path, notes_root, assets_dir, copied_images
        )
        
        # Compute relative path from new note location to asset
        rel_path = compute_relative_path(current_note_path, target_path)
        
        return f'![{alt_text}]({rel_path})'
    
    return re.sub(pattern, replace_image, content)


def process_note(
    note_path: Path,
    notes_root: Path,
    docs_dir: Path,
    assets_dir: Path,
    note_mapping: Dict[str, Path],
    copied_images: Set[str]
):
    """
    Process a single note: read, rewrite links, write to new location.
    """
    # Read original content
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Get new path
    new_path = note_mapping[get_note_key(note_path)]
    new_full_path = docs_dir / new_path.relative_to(docs_dir) if new_path.is_relative_to(docs_dir) else new_path
    
    # Rewrite wikilinks
    content = rewrite_wikilinks(
        content, new_path, note_path, notes_root, docs_dir, assets_dir, note_mapping, copied_images
    )
    
    # Rewrite Markdown images
    content = rewrite_markdown_images(
        content, new_path, note_path, notes_root, docs_dir, assets_dir, copied_images
    )
    
    # Write to new location
    new_full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(new_full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return new_full_path


def create_index(notes_root: Path, docs_dir: Path):
    """
    Create docs/index.md from root README.md if it exists.
    """
    readme_path = notes_root / 'README.md'
    index_path = docs_dir / 'index.md'
    
    if readme_path.exists():
        shutil.copy2(readme_path, index_path)
        print(f"Created {index_path} from {readme_path}")
    else:
        # Create a placeholder
        index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("# Documentation\n\nWelcome to the documentation.\n")
        print(f"Created placeholder {index_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Migrate Obsidian notes to GitBook format'
    )
    parser.add_argument(
        '--notes-root',
        type=str,
        default='.',
        help='Root directory of Obsidian notes (default: current directory)'
    )
    parser.add_argument(
        '--docs-dir',
        type=str,
        default='docs',
        help='Output directory for GitBook docs (default: docs)'
    )
    parser.add_argument(
        '--assets-subdir',
        type=str,
        default='assets',
        help='Subdirectory for assets within docs-dir (default: assets)'
    )
    parser.add_argument(
        '--ignore-dir',
        action='append',
        default=[],
        help='Directories to ignore (can be specified multiple times)'
    )
    parser.add_argument(
        '--filter-folder',
        type=str,
        default=None,
        help='Only migrate notes from this specific folder (e.g., "DevOps")'
    )
    
    args = parser.parse_args()
    
    # Set default ignore directories
    if not args.ignore_dir:
        args.ignore_dir = ['.git', '.obsidian', '.trash', '.makemd', '.space', 'docs']
    
    # Convert to absolute paths
    notes_root = Path(args.notes_root).resolve()
    docs_dir = Path(args.docs_dir).resolve()
    assets_dir = docs_dir / args.assets_subdir
    
    print(f"Notes root: {notes_root}")
    print(f"Docs directory: {docs_dir}")
    print(f"Assets directory: {assets_dir}")
    print(f"Ignoring: {', '.join(args.ignore_dir)}")
    if args.filter_folder:
        print(f"Filtering to folder: {args.filter_folder}")
    print()
    
    # Find all notes
    all_notes = find_all_notes(notes_root, args.ignore_dir)
    
    # Filter by folder if specified
    if args.filter_folder:
        filter_path = notes_root / args.filter_folder
        all_notes = [n for n in all_notes if n.is_relative_to(filter_path)]
        print(f"Found {len(all_notes)} notes in {args.filter_folder}")
    else:
        print(f"Found {len(all_notes)} notes")
    
    if not all_notes:
        print("No notes found to migrate.")
        return
    
    # Build note mapping
    note_mapping = build_note_mapping(all_notes, notes_root, docs_dir)
    
    # Track copied images to avoid duplicates
    copied_images: Set[str] = set()
    
    # Process each note
    processed_count = 0
    for note_path in all_notes:
        try:
            new_path = process_note(
                note_path, notes_root, docs_dir, assets_dir, note_mapping, copied_images
            )
            processed_count += 1
            print(f"Processed: {note_path.relative_to(notes_root)} -> {new_path.relative_to(docs_dir)}")
        except Exception as e:
            print(f"Error processing {note_path}: {e}")
    
    # Create index.md
    create_index(notes_root, docs_dir)
    
    print()
    print(f"Migration complete!")
    print(f"  {processed_count} notes processed")
    print(f"  {len(copied_images)} images copied")
    print(f"  Output directory: {docs_dir}")


if __name__ == '__main__':
    main()
