"""Clean old Wowchemy project items for Hugo Blox v0.12 compatibility.

- Strips unused fields (url_video, url_code, url_pdf, url_slides, slides, summary, links comments)
- Keeps: title, tags, date, external_link, image
- Removes empty/commented fields
"""

import os
import re
import yaml
import glob

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "content", "en")
SECTIONS = ["blog", "news", "media", "tutorials"]

def clean_item(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Split frontmatter and body
    parts = content.split("---", 2)
    if len(parts) < 3:
        print(f"  SKIP (no frontmatter): {filepath}")
        return

    fm_raw = parts[1]
    body = parts[2].strip()

    try:
        fm = yaml.safe_load(fm_raw)
    except yaml.YAMLError as e:
        print(f"  ERROR parsing {filepath}: {e}")
        return

    if not fm:
        print(f"  SKIP (empty frontmatter): {filepath}")
        return

    # Build clean frontmatter
    clean = {}
    if "title" in fm:
        clean["title"] = fm["title"]
    if "tags" in fm and fm["tags"]:
        clean["tags"] = fm["tags"]
    if "date" in fm:
        clean["date"] = str(fm["date"])
    if "external_link" in fm and fm["external_link"]:
        clean["external_link"] = fm["external_link"]
    if "image" in fm and fm["image"]:
        img = {}
        if fm["image"].get("caption"):
            img["caption"] = fm["image"]["caption"]
        if fm["image"].get("focal_point"):
            img["focal_point"] = fm["image"]["focal_point"]
        if img:
            clean["image"] = img

    # Write clean file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("---\n")
        f.write(yaml.dump(clean, default_flow_style=False, allow_unicode=True, sort_keys=False))
        f.write("---\n")
        if body:
            f.write("\n" + body + "\n")

    print(f"  OK: {os.path.basename(os.path.dirname(filepath))}")

for section in SECTIONS:
    section_dir = os.path.join(CONTENT_DIR, section)
    print(f"\n=== {section} ===")
    for item_dir in sorted(glob.glob(os.path.join(section_dir, "*", "index.md"))):
        clean_item(item_dir)

print("\nDone!")
