# Obsidian to GitBook Migration Script

This script converts Obsidian-style notes to GitBook format, handling filenames, links, and images.

## Features

- **Kebab-case conversion**: Converts folder and file names to lowercase kebab-case
- **Image handling**: 
  - Copies images to `docs/assets/` with organized subdirectories
  - Handles URL-encoded filenames (e.g., `%20` spaces)
  - Searches common Obsidian image locations (Assets, attachments subdirectories)
  - Rewrites image links with correct relative paths
- **Link rewriting**:
  - Converts Obsidian wikilinks `[[Note Title]]` to Markdown links
  - Converts image embeds `![[image.png]]` to Markdown images
  - Preserves aliases: `[[Note|Alias]]` → `[Alias](path)`
  - Handles standard Markdown image links
- **Idempotent**: Safe to run multiple times without creating duplicates

## Usage

### Basic Usage

Migrate all notes from the repository root:

```bash
python3 scripts/obsidian_to_gitbook.py
```

### Filter by Folder

Migrate only a specific folder (e.g., DevOps):

```bash
python3 scripts/obsidian_to_gitbook.py --filter-folder DevOps
```

### Custom Options

```bash
python3 scripts/obsidian_to_gitbook.py \
  --notes-root /path/to/obsidian/vault \
  --docs-dir output/docs \
  --assets-subdir images \
  --ignore-dir .git \
  --ignore-dir .obsidian \
  --filter-folder MyFolder
```

## Arguments

- `--notes-root`: Root directory of Obsidian notes (default: current directory)
- `--docs-dir`: Output directory for GitBook docs (default: `docs`)
- `--assets-subdir`: Subdirectory for assets within docs-dir (default: `assets`)
- `--ignore-dir`: Directories to ignore (can be specified multiple times)
  - Default: `.git`, `.obsidian`, `.trash`, `.makemd`, `.space`, `docs`
- `--filter-folder`: Only migrate notes from this specific folder

## Output Structure

```
docs/
├── assets/
│   └── <original-folder-structure>/
│       └── images...
├── <folder-name>/
│   ├── <subfolder-name>/
│   │   └── note-file.md
│   └── another-note.md
└── index.md
```

## Examples

### Example 1: Migrate DevOps folder

```bash
cd /path/to/MyNotes
python3 scripts/obsidian_to_gitbook.py --filter-folder DevOps
```

Result:
- `DevOps/Kafka/Kafka-For-Beginners.md` → `docs/devops/kafka/kafka-for-beginners.md`
- `DevOps/Kafka/Assets/Pasted image 20240401065054.png` → `docs/assets/DevOps/Kafka/Pasted image 20240401065054.png`
- Images references updated: `![](Pasted%20image%2020240401065054.png)` → `![](../../assets/DevOps/Kafka/Pasted image 20240401065054.png)`

### Example 2: Migrate entire repository

```bash
cd /path/to/MyNotes
python3 scripts/obsidian_to_gitbook.py
```

This will migrate all folders except those in the ignore list.

## Migration Behavior

### Filename Normalization

- **Original**: `AWS Solution Architect (v2)/AWS EBS & EFS.md`
- **Normalized**: `docs/aws-solution-architect-v2/aws-ebs-efs.md`

### Image Link Rewriting

**Original markdown:**
```markdown
![](Pasted%20image%2020240401065054.png)
```

**Migrated markdown:**
```markdown
![](../../assets/DevOps/Kafka/Pasted image 20240401065054.png)
```

### Wikilink Conversion

**Original:**
```markdown
See [[Kubernetes Overview]] for more details.
```

**Migrated:**
```markdown
See [Kubernetes Overview](../kubernetes/kubernetes-overview.md) for more details.
```

## Notes

- The script preserves the original files - it only creates new files in `docs/`
- Images are copied (not moved) to maintain the original vault
- The script is idempotent - running it multiple times won't create duplicates
- External URLs (http://, https://) are left unchanged
- Only image files are processed for attachments (png, jpg, jpeg, gif, svg, webp, bmp)

## Troubleshooting

### Images not found

If you see "Warning: Image not found", the script couldn't locate the image. Check:
1. The image file exists in the original location
2. The filename matches exactly (case-sensitive)
3. The image is in the same directory or an Assets/attachments subdirectory

### Wikilinks not resolved

If you see "Warning: Could not resolve wikilink", the target note wasn't found. Check:
1. The target note exists in the filtered folders
2. The note name matches the wikilink text (case-insensitive)
3. The target note isn't in an ignored directory
