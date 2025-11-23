import os
import re

BASE_DIR = "notes/ctf-notes"

def cleanup_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    new_lines = []
    skip_next_empty = False
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Remove "Copy" lines that appear before code blocks
        if stripped == "Copy":
            continue
            
        # Remove "Last updated" lines
        if stripped.lower().startswith("last updated"):
            continue
            
        # Remove breadcrumb navigation (e.g., "1. [AppSec](/ctf-notes)")
        if re.match(r'^\d+\.\s+\[.*\]\(.*\)$', stripped):
            continue
            
        # Remove Previous/Next navigation links at the bottom
        if re.match(r'^\[Previous.*\]\(.*\)\[Next.*\]\(.*\)$', stripped):
            continue
            
        # Remove lines that are just a single number and a dot (sometimes artifacts of lists)
        if re.match(r'^\d+\.$', stripped):
            continue

        new_lines.append(line)

    # Remove multiple consecutive empty lines and duplicate headings
    final_lines = []
    prev_empty = False
    seen_headings = set()
    
    # We want to allow headings if they are different, but if we see the exact same heading 
    # content (e.g. "# Fuzzing") multiple times at the start of the file, we should remove duplicates.
    # However, a heading might appear later in a different context. 
    # Given the specific issue is likely the title being repeated at the top:
    
    first_heading_found = False
    
    for i, line in enumerate(new_lines):
        stripped = line.strip()
        
        if stripped == "":
            if prev_empty:
                continue
            prev_empty = True
            final_lines.append(line)
            continue
            
        # Check for duplicate top-level headings
        if stripped.startswith("# "):
            if not first_heading_found:
                first_heading_found = True
                seen_headings.add(stripped)
                prev_empty = False
                final_lines.append(line)
            else:
                # If we've already seen this exact top-level heading, skip it
                if stripped in seen_headings:
                    continue
                else:
                    prev_empty = False
                    final_lines.append(line)
        else:
            prev_empty = False
            final_lines.append(line)

    with open(file_path, 'w') as f:
        f.writelines(final_lines)
    print(f"Cleaned {file_path}")

def main():
    for root, dirs, files in os.walk(BASE_DIR):
        for file in files:
            if file.endswith(".md"):
                cleanup_file(os.path.join(root, file))

if __name__ == "__main__":
    main()
