import os, re, yaml

old_dir = r"C:\Users\rt3105\Documents\GitHub\starter-academic\content\en\publication"
new_dir = r"C:\Users\rt3105\Documents\GitHub\prime-fox\content\en\publications"

for name in sorted(os.listdir(old_dir)):
    src = os.path.join(old_dir, name, "index.md")
    if not os.path.isfile(src):
        continue
    
    with open(src, "r", encoding="utf-8") as f:
        raw = f.read()
    
    # Split frontmatter and body
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", raw, re.DOTALL)
    if not m:
        print(f"SKIP: {name}")
        continue
    
    fm_raw = m.group(1)
    body = m.group(2).strip()
    
    # Parse YAML frontmatter
    try:
        data = yaml.safe_load(fm_raw)
    except:
        print(f"YAML ERROR: {name}")
        continue
    
    if not isinstance(data, dict):
        print(f"SKIP (not dict): {name}")
        continue
    
    title = data.get("title", "")
    authors = data.get("authors", [])
    date = data.get("date", "")
    doi = data.get("doi", "")
    abstract = data.get("abstract", "")
    add_badge = data.get("add_badge", True)
    author_notes = data.get("author_notes", None)
    
    # Clean publication field - strip HTML
    pub = data.get("publication", "")
    if pub:
        pub = re.sub(r"<a [^>]*>", "", pub)
        pub = re.sub(r"</a>", "", pub)
        pub = pub.strip()
    
    # Collect links
    links = []
    
    # Original named links
    old_links = data.get("links", [])
    if old_links:
        for lk in old_links:
            if isinstance(lk, dict) and lk.get("name") and lk.get("url"):
                url = lk["url"].strip()
                if url and url != "#":
                    links.append({"name": lk["name"].strip(), "url": url})
    
    # Convert url_* fields
    for field, label in [("url_code", "Code"), ("url_dataset", "Dataset"), 
                         ("url_video", "Video"), ("url_project", "Project")]:
        val = data.get(field)
        if val and isinstance(val, str) and val.strip() and val.strip() != "#":
            links.append({"name": label, "url": val.strip()})
    
    # url_pdf only if no PDF link exists
    url_pdf = data.get("url_pdf")
    if url_pdf and isinstance(url_pdf, str) and url_pdf.strip() and url_pdf.strip() != "#":
        has_pdf = any(l["name"] == "PDF" for l in links)
        if not has_pdf:
            links.append({"name": "PDF", "url": url_pdf.strip()})
    
    # Build new frontmatter
    lines = []
    lines.append("---")
    
    # Title - escape internal quotes
    safe_title = title.replace('"', '\\"')
    lines.append(f'title: "{safe_title}"')
    
    # Authors
    lines.append("authors:")
    for a in authors:
        if isinstance(a, str):
            lines.append(f'  - "{a}"')
    
    # Author notes
    if author_notes:
        lines.append("author_notes:")
        for an in author_notes:
            lines.append(f'  - "{an}"')
    
    # Date
    if date:
        if hasattr(date, 'isoformat'):
            date = date.isoformat()
        lines.append(f'date: "{date}"')
    
    # Publication type
    lines.append('publication_types: ["article-journal"]')
    
    # Publication
    safe_pub = pub.replace('"', '\\"')
    lines.append(f'publication: "{safe_pub}"')
    
    # Abstract
    if abstract:
        safe_abs = abstract.replace('"', '\\"')
        lines.append(f'abstract: "{safe_abs}"')
    
    lines.append("featured: true")
    
    if add_badge:
        lines.append("add_badge: true")
    
    # hugoblox ids
    if doi:
        lines.append("hugoblox:")
        lines.append("  ids:")
        lines.append(f'    doi: "{doi}"')
    
    # Links
    if links:
        lines.append("links:")
        for lk in links:
            lines.append(f'  - name: "{lk["name"]}"')
            lines.append(f'    url: "{lk["url"]}"')
    
    lines.append("---")
    
    # Write output
    out_dir = os.path.join(new_dir, name)
    os.makedirs(out_dir, exist_ok=True)
    
    content = "\n".join(lines)
    if body:
        content += "\n\n" + body + "\n"
    else:
        content += "\n"
    
    with open(os.path.join(out_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"OK: {name} ({len(authors)} authors, {len(links)} links)")

print("\nDone!")
