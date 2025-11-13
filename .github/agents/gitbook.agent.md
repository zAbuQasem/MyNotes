name: "obsidian-to-gitbook"
description: >
  Convert this Obsidian-based vault (MyNotes) to a GitBook-friendly layout:
  - Scan markdown notes from the repo root (excluding .obsidian/.makemd/.space/.trash/docs/.git)
  - Create a docs/ tree with kebab-case filenames
  - Move/normalize image references into docs/assets/
  - Rewrite Obsidian-style wikilinks to standard Markdown links

instructions: |
  You are a migration assistant for the zAbuQasem/MyNotes repository.

  Goals:
  - All documentation content should be under docs/
  - All images and other attachments referenced from notes should live under docs/assets/
  - File names should be kebab-case and end with .md
  - Obsidian-style links and embeds:
      [[Note Title]]
      [[Note Title|Alias]]
      ![[image.png]]
      ![[image.png|Alt text]]
    must be converted to standard Markdown links/images.
  - Standard Markdown image links like:
      ![alt](relative/path/to/image.png)
    should be rewritten to point into docs/assets/, and the images
    should be copied there.

  Repository-specific assumptions:
  - The vault root is the repo root (".").
  - Ignore these directories when looking for notes:
      .git, .obsidian, .trash, .makemd, .space, docs
  - Topic folders like "AWS Pentesting", "Active Directory", "DevOps",
    etc. contain the real notes and possibly images.
  - There is already a top-level README.md; use it as the basis
    for docs/index.md if index.md does not exist.

  Implementation details:
  - Use the Python script at scripts/obsidian_to_gitbook.py as the canonical
    migration tool.
  - The script must:
      * Walk all *.md files under the vault root (except in ignored dirs).
      * Build a mapping from note name → new docs/ path.
      * For each note, rewrite:
          - wikilinks to other notes using the mapping.
          - image links to copy the underlying file to docs/assets/
            (preserving sub-paths relative to the vault root), and
            adjust the link paths accordingly.
      * Write the rewritten notes under docs/ with kebab-case paths.
      * Create docs/index.md if missing (using README.md).

  Non-goals:
  - Do not implement GitBook hosting configuration or CI here.
  - Do not touch non-doc code or unrelated files.

  When editing files:
  - Keep the script idempotent: running it multiple times should not break links.
  - Prefer small, focused commits for the migration.
  - Describe the migration clearly in the commit message / PR description.

trigger:
  manual: true

inputs:
  - name: notes_root
    description: "Root directory of the Obsidian vault"
    default: "."
  - name: docs_dir
    description: "Target GitBook docs directory"
    default: "docs"
  - name: assets_subdir
    description: "Subdirectory under docs_dir for media/attachments"
    default: "assets"

actions:
  - name: inspect_repo
    description: "Inspect the current repository to confirm structure"
    steps:
      - run: ls -R
        shell: bash

  - name: ensure_script
    description: "Create or update the obsidian_to_gitbook.py migration script"
    steps:
      - run: mkdir -p scripts
        shell: bash
      - run: |
          cat > scripts/obsidian_to_gitbook.py << 'EOF'
          #!/usr/bin/env python3
          """
          Obsidian-style vault -> GitBook-style docs/ migration for MyNotes.

          - Treat the repo root as the Obsidian vault root.
          - Ignore internal/plugin dirs like .obsidian/.makemd/.space/.trash/docs/.git.
          - Convert all *.md notes to docs/ with kebab-case paths.
          - Rewrite Obsidian wikilinks and standard image links.
          - Copy referenced images into docs/assets/ (preserving sub-paths).
          """

          import argparse
          import os
          import re
          import shutil
          from pathlib import Path

          IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp")
          WIKILINK_RE = re.compile(r"(!)?\[\[([^\]|]+)(\|([^\]]+))?\]\]")
          MD_LINK_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")

          def kebab_case_path(rel: Path) -> Path:
              parts = []
              for part in rel.parts:
                  stem, dot, ext = part.partition(".")
                  stem = re.sub(r"[\s_]+", "-", stem)
                  stem = re.sub(r"[^a-zA-Z0-9\-]", "", stem)
                  if ext:
                      parts.append((stem.lower() or "index") + "." + ext)
                  else:
                      parts.append(stem.lower() or "index")
              return Path(*parts)

          def collect_notes(notes_root: Path, ignore_dirs=None):
              ignore_dirs = set(ignore_dirs or [])
              notes = []
              for path in notes_root.rglob("*.md"):
                  if any(part in ignore_dirs for part in path.parts):
                      continue
                  notes.append(path)
              return notes

          def build_note_map(notes, notes_root: Path, docs_dir: Path):
              note_map = {}
              for src in notes:
                  rel = src.relative_to(notes_root)
                  dst_rel = kebab_case_path(rel)
                  note_key = src.stem.lower()
                  note_map[note_key] = os.fspath(dst_rel)
              return note_map

          def rewrite_content(
              text: str,
              src_note: Path,
              notes_root: Path,
              docs_dir: Path,
              dst_path: Path,
              note_map: dict,
              assets_dir: Path,
          ):
              # Compute relative path from this doc to assets dir
              assets_rel = os.path.relpath(assets_dir, dst_path.parent)

              def move_attachment(attachment_path: Path) -> str | None:
                  if not attachment_path.exists():
                      return None
                  if attachment_path.suffix.lower() not in IMAGE_EXTENSIONS:
                      return None
                  rel_from_root = attachment_path.resolve().relative_to(notes_root.resolve())
                  target = assets_dir / rel_from_root
                  target.parent.mkdir(parents=True, exist_ok=True)
                  if not target.exists():
                      shutil.copy2(attachment_path, target)
                  # Path relative to dst_path
                  return os.path.join(assets_rel, os.fspath(rel_from_root))

              # 1) Rewrite standard markdown image links
              def md_link_repl(match):
                  alt = match.group(1)
                  url = match.group(2).strip()
                  # Ignore absolute URLs
                  if re.match(r"^[a-zA-Z]+://", url):
                      return match.group(0)
                  attachment_src = (src_note.parent / url).resolve()
                  new_rel = move_attachment(attachment_src)
                  if not new_rel:
                      return match.group(0)
                  return f"![{alt}]({new_rel})"

              text = MD_LINK_RE.sub(md_link_repl, text)

              # 2) Rewrite Obsidian wikilinks
              def wiki_repl(match):
                  is_embed = match.group(1) == "!"
                  target = match.group(2).strip()
                  alias = match.group(4)

                  # If target looks like an image filename, treat as local attachment
                  if any(target.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                      attachment_src = (src_note.parent / target).resolve()
                      new_rel = move_attachment(attachment_src)
                      alt_text = alias or Path(target).stem
                      if new_rel:
                          return f"![{alt_text}]({new_rel})"
                      return match.group(0)

                  # Otherwise, it's a note
                  note_key = Path(target).stem.lower()
                  if note_key in note_map:
                      rel_to_note = os.path.relpath(docs_dir / note_map[note_key], dst_path.parent)
                      link_text = alias or Path(target).stem
                      return f"[{link_text}]({rel_to_note})"

                  return match.group(0)

              text = WIKILINK_RE.sub(wiki_repl, text)
              return text

          def ensure_index(docs_dir: Path, notes_root: Path):
              index_md = docs_dir / "index.md"
              if index_md.exists():
                  return
              root_readme = Path("README.md")
              if root_readme.exists():
                  index_md.write_text(root_readme.read_text(encoding="utf-8"), encoding="utf-8")
              else:
                  index_md.write_text(
                      "# Documentation\n\nMigrated from Obsidian vault.\n",
                      encoding="utf-8",
                  )

          def main():
              parser = argparse.ArgumentParser(
                  description="Migrate Obsidian-style repo to GitBook-style docs/ layout."
              )
              parser.add_argument(
                  "--notes-root",
                  default=".",
                  help="Root directory for notes (where your Obsidian vault lives)",
              )
              parser.add_argument(
                  "--docs-dir",
                  default="docs",
                  help="Target docs directory",
              )
              parser.add_argument(
                  "--assets-subdir",
                  default="assets",
                  help="Assets subdirectory under docs",
              )
              parser.add_argument(
                  "--ignore-dir",
                  action="append",
                  default=[".git", ".obsidian", ".trash", ".makemd", ".space", "docs"],
                  help="Directory names to ignore (can be passed multiple times)",
              )
              args = parser.parse_args()

              notes_root = Path(args.notes_root).resolve()
              docs_dir = Path(args.docs_dir).resolve()
              assets_dir = docs_dir / args.assets_subdir

              notes = collect_notes(notes_root, ignore_dirs=args.ignore_dir)
              if not notes:
                  raise SystemExit(f"No markdown files found under {notes_root}")

              note_map = build_note_map(notes, notes_root, docs_dir)

              for src in notes:
                  rel = src.relative_to(notes_root)
                  dst_rel = kebab_case_path(rel)
                  dst = docs_dir / dst_rel
                  dst.parent.mkdir(parents=True, exist_ok=True)

                  text = src.read_text(encoding="utf-8")
                  rewritten = rewrite_content(
                      text=text,
                      src_note=src,
                      notes_root=notes_root,
                      docs_dir=docs_dir,
                      dst_path=dst,
                      note_map=note_map,
                      assets_dir=assets_dir,
                  )
                  dst.write_text(rewritten, encoding="utf-8")

              ensure_index(docs_dir, notes_root)
              print("Migration complete.")
              print(f"Docs root: {docs_dir}")
              print(f"Assets root: {assets_dir}")

          if __name__ == "__main__":
              main()
          EOF
        shell: bash
      - run: chmod +x scripts/obsidian_to_gitbook.py
        shell: bash

  - name: run_migration
    description: "Execute the Obsidian -> GitBook migration script with the provided inputs"
    steps:
      - run: |
          python scripts/obsidian_to_gitbook.py \
            --notes-root "${{ inputs.notes_root }}" \
            --docs-dir "${{ inputs.docs_dir }}" \
            --assets-subdir "${{ inputs.assets_subdir }}"
        shell: bash

  - name: show_result
    description: "List resulting docs/ structure"
    steps:
      - run: ls -R "${{ inputs.docs_dir }}"
        shell: bash
