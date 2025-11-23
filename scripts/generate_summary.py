import os

def get_title(file_path):
    """Extract title from the first line of the markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line.startswith('# '):
                return first_line[2:].strip()
    except Exception:
        pass
    # Fallback to filename
    name = os.path.basename(file_path)
    return os.path.splitext(name)[0].replace('-', ' ').title()

def generate_summary_section(base_dir, relative_path, level=0):
    """Recursively generate summary entries."""
    entries = []
    full_path = os.path.join(base_dir, relative_path)
    
    # Get all items in directory
    try:
        items = sorted(os.listdir(full_path))
    except FileNotFoundError:
        return []

    # Separate files and directories
    files = []
    dirs = []
    
    for item in items:
        if item.startswith('.'): continue
        item_path = os.path.join(full_path, item)
        if os.path.isdir(item_path):
            dirs.append(item)
        elif item.endswith('.md') and item.lower() != 'readme.md':
            files.append(item)
            
    # Process files first (or after? usually mixed, but let's do files then dirs)
    # Actually, usually we want the README of the dir to be the section header
    
    # Check if there is a readme.md in this dir
    readme_path = os.path.join(full_path, 'readme.md')
    if not os.path.exists(readme_path):
        readme_path = os.path.join(full_path, 'README.md')
        
    indent = '  ' * level
    
    # If this is not the root notes dir, add the section header
    if relative_path != '.':
        title = os.path.basename(relative_path).replace('-', ' ').title()
        # If readme exists, use its title
        if os.path.exists(readme_path):
            title = get_title(readme_path)
            link = os.path.join('notes', relative_path, 'readme.md')
            entries.append(f"{indent}* [{title}]({link})")
        else:
            entries.append(f"{indent}* {title}")
    
    # Add files
    for file in files:
        file_path = os.path.join(full_path, file)
        title = get_title(file_path)
        link = os.path.join('notes', relative_path, file)
        entries.append(f"{indent}  * [{title}]({link})")
        
    # Recurse into directories
    for d in dirs:
        # Skip attachments or assets folders if they don't contain notes
        if d.lower() in ['attachments', 'assets', 'images', 'img']:
            continue
            
        new_relative = os.path.join(relative_path, d)
        # If we are at root, we don't indent yet, we just call recursively
        if relative_path == '.':
            entries.extend(generate_summary_section(base_dir, new_relative, level))
        else:
            entries.extend(generate_summary_section(base_dir, new_relative, level + 1))
            
    return entries

def main():
    base_dir = 'notes'
    
    print("# Table of Contents\n")
    print("* [Introduction](readme.md)\n")
    
    # We want to group by the top-level folders in 'notes' as main sections
    # Get top level dirs in notes
    top_dirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and not d.startswith('.')])
    
    for d in top_dirs:
        # Create a header for the top level directory
        # Check if it has a readme
        readme_path = os.path.join(base_dir, d, 'readme.md')
        title = d.replace('-', ' ').title()
        if os.path.exists(readme_path):
            title = get_title(readme_path)
            
        print(f"## {title}\n")
        
        # Now generate children
        # We pass the directory as the relative path
        # Level 0 because we are under a ## Header
        entries = generate_summary_section(base_dir, d, level=0)
        
        # The first entry from generate_summary_section for the top dir itself might be redundant 
        # if we just printed the header.
        # generate_summary_section adds the dir itself as a link if it has a readme.
        # Let's adjust generate_summary_section or handle it here.
        
        # Actually, let's use a slightly different approach for top level
        # We want the top level folder to be the ## Header
        # And then list its contents.
        # If the top level folder has a readme, we usually want that as the first item or as the header link?
        # GitBook headers usually aren't links.
        
        # Let's manually add the readme link if it exists
        if os.path.exists(readme_path):
             print(f"* [{title}](notes/{d}/readme.md)")
        
        # Now get contents inside
        # We need to list files in d and subdirs in d
        
        # Get files in d (excluding readme)
        files = sorted([f for f in os.listdir(os.path.join(base_dir, d)) if f.endswith('.md') and f.lower() != 'readme.md'])
        for f in files:
            f_path = os.path.join(base_dir, d, f)
            f_title = get_title(f_path)
            print(f"* [{f_title}](notes/{d}/{f})")
            
        # Get subdirs in d
        subdirs = sorted([sd for sd in os.listdir(os.path.join(base_dir, d)) if os.path.isdir(os.path.join(base_dir, d, sd)) and not sd.startswith('.') and sd.lower() not in ['attachments', 'assets']])
        
        for sd in subdirs:
            # For subdirectories, we use the recursive function
            # We want them to start at indentation 0 relative to the section, or indented?
            # Usually:
            # ## Section
            # * [Main Page](...)
            # * [Sub Page](...)
            # * [Sub Dir](...)
            #   * [Sub Sub Page](...)
            
            # So subdirs should be treated as items
            sub_entries = generate_summary_section(base_dir, os.path.join(d, sd), level=0)
            for entry in sub_entries:
                print(entry)
                
        print("") # Newline after section

if __name__ == "__main__":
    main()
