"""
Clean deprecated fields from FR publication files.
For each FR publication, read the corresponding EN file (already clean)
and replace the FR frontmatter with the EN frontmatter, keeping only the
French abstract and publication text.
"""
import os
import re
import yaml
import sys

FR_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'fr', 'publications')
EN_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'en', 'publications')

# Fields to remove from FR publications
DEPRECATED_FIELDS = [
    'doi', 'url_code', 'url_dataset', 'url_pdf', 'url_project',
    'url_video', 'slides', 'external_link', 'math', 'tags',
    'publication_short',
]


def parse_frontmatter(filepath):
    """Parse YAML frontmatter from a markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match YAML frontmatter between --- delimiters
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None, content
    
    fm_text = match.group(1)
    try:
        fm = yaml.safe_load(fm_text)
    except yaml.YAMLError as e:
        print(f"  YAML error in {filepath}: {e}")
        return None, content
    
    return fm, content


def build_clean_frontmatter(en_fm, fr_fm):
    """
    Build clean frontmatter by taking the EN file as base
    and swapping in the French abstract and publication text.
    """
    result = dict(en_fm)  # Start with EN (clean format)
    
    # Keep FR abstract if it exists and differs from EN
    if 'abstract' in fr_fm and fr_fm['abstract']:
        result['abstract'] = fr_fm['abstract']
    
    # Keep FR publication text if it differs (might have HTML links)
    # But use the clean EN format
    # result['publication'] already comes from EN which is clean
    
    return result


def write_clean_file(filepath, fm):
    """Write a clean publication file with proper YAML frontmatter."""
    # Custom YAML dumper to handle multiline strings properly
    class CustomDumper(yaml.SafeDumper):
        pass
    
    def str_representer(dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        if any(c in data for c in [':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']):
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)
    
    CustomDumper.add_representer(str, str_representer)
    
    # Build ordered output manually for readability
    lines = ['---']
    
    # Title
    lines.append(f'title: "{fm["title"]}"')
    
    # Authors
    lines.append('authors:')
    for author in fm.get('authors', []):
        lines.append(f'  - "{author}"')
    
    # Date
    lines.append(f'date: "{fm["date"]}"')
    
    # Publication types
    pt = fm.get('publication_types', ['article-journal'])
    lines.append(f'publication_types: ["{pt[0]}"]')
    
    # Publication
    pub = fm.get('publication', '')
    lines.append(f'publication: "{pub}"')
    
    # Abstract
    abstract = fm.get('abstract', '')
    if abstract:
        # Use literal block scalar for multiline
        lines.append('abstract: |-')
        for aline in abstract.split('\n'):
            lines.append(f'  {aline}')
    
    # Featured
    if fm.get('featured'):
        lines.append('featured: true')
    
    # Add badge
    if fm.get('add_badge'):
        lines.append('add_badge: true')
    
    # Hugo Blox IDs
    hugoblox = fm.get('hugoblox', {})
    if hugoblox and hugoblox.get('ids'):
        lines.append('hugoblox:')
        lines.append('  ids:')
        for key, val in hugoblox['ids'].items():
            lines.append(f'    {key}: "{val}"')
    
    # Links
    links = fm.get('links', [])
    if links:
        lines.append('links:')
        for link in links:
            name = link.get('name', '')
            url = link.get('url', '')
            lines.append(f'  - name: "{name}"')
            lines.append(f'    url: "{url}"')
    
    lines.append('---')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


def main():
    fr_pubs = sorted([d for d in os.listdir(FR_DIR) 
                      if os.path.isdir(os.path.join(FR_DIR, d)) and d != '_index.md'])
    
    cleaned = 0
    skipped = 0
    errors = 0
    
    for pub_dir in fr_pubs:
        fr_file = os.path.join(FR_DIR, pub_dir, 'index.md')
        en_file = os.path.join(EN_DIR, pub_dir, 'index.md')
        
        if not os.path.exists(fr_file):
            continue
        
        if not os.path.exists(en_file):
            print(f"  SKIP {pub_dir}: no EN counterpart")
            skipped += 1
            continue
        
        print(f"  Processing {pub_dir}...")
        
        en_fm, _ = parse_frontmatter(en_file)
        fr_fm, _ = parse_frontmatter(fr_file)
        
        if not en_fm or not fr_fm:
            print(f"  ERROR {pub_dir}: could not parse frontmatter")
            errors += 1
            continue
        
        clean_fm = build_clean_frontmatter(en_fm, fr_fm)
        write_clean_file(fr_file, clean_fm)
        cleaned += 1
    
    print(f"\nDone: {cleaned} cleaned, {skipped} skipped, {errors} errors")


if __name__ == '__main__':
    main()
