import os
import re
import urllib.parse

def find_markdown_files(root_dir):
    markdown_files = []
    for root, dirs, files in os.walk(root_dir):
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    return markdown_files

def check_links(file_path, root_dir):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex for markdown links [text](url) and images ![alt](url)
    # This is a simple regex and might miss some edge cases, but good for a start
    link_pattern = re.compile(r'\[.*?\]\((.*?)\)')
    
    links = link_pattern.findall(content)
    broken_links = []

    for link in links:
        # Ignore external links
        if link.startswith('http://') or link.startswith('https://') or link.startswith('mailto:'):
            continue
        
        # Ignore empty links or just anchors
        if not link or link.startswith('#'):
            continue

        # Handle anchors in file paths
        url_parts = link.split('#')
        file_part = url_parts[0]
        
        if not file_part:
            continue

        # Decode URL (e.g. %20 to space)
        file_part = urllib.parse.unquote(file_part)

        # Resolve path
        # If it starts with /, it's relative to root (GitBook behavior usually)
        # If not, it's relative to current file
        if file_part.startswith('/'):
            target_path = os.path.join(root_dir, file_part.lstrip('/'))
        else:
            target_path = os.path.join(os.path.dirname(file_path), file_part)
        
        # Normalize path to remove ../ and ./
        target_path = os.path.normpath(target_path)

        if not os.path.exists(target_path):
            broken_links.append((link, target_path))

    return broken_links

def main():
    root_dir = os.getcwd()
    markdown_files = find_markdown_files(root_dir)
    
    all_broken_links = {}
    
    for file in markdown_files:
        broken = check_links(file, root_dir)
        if broken:
            all_broken_links[file] = broken

    if all_broken_links:
        print("Found broken links:")
        for file, links in all_broken_links.items():
            print(f"\nIn file: {os.path.relpath(file, root_dir)}")
            for link, target in links:
                print(f"  - Link: {link}")
                print(f"    Target: {target}")
    else:
        print("No broken links found.")

if __name__ == "__main__":
    main()
