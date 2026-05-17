"""Parse Obsidian markdown: frontmatter, content, wiki links."""
import os
import re
import urllib.parse
import yaml

from config import VAULT_PATH, EXCLUDED_FILES


def parse_markdown(filepath):
    """Return (frontmatter_dict, body_content)."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    frontmatter = {}
    body = raw

    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
            except Exception:
                frontmatter = {}
            body = parts[2]

    return frontmatter, body


def extract_links(content, current_rel_path):
    """Extract internal markdown/Obsidian links from content."""
    links = []

    # Standard markdown: [text](/path/to/File.md) or [text](path/to/File.md)
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", content):
        href = m.group(2).strip()
        if href.startswith("http://") or href.startswith("https://"):
            continue
        links.append(href)

    # Obsidian wiki links: [[path|alias]] or [[path]]
    for m in re.finditer(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", content):
        links.append(m.group(1).strip())

    return links


def path_to_doc_id(rel_path):
    """Convert 'knowledge/PHK Sepanjang 2025.md' → 'knowledge-phk-sepanjang-2025'."""
    base = rel_path[:-3] if rel_path.endswith(".md") else rel_path
    base = urllib.parse.unquote(base)
    doc_id = re.sub(r"[/\\]", "-", base)
    doc_id = re.sub(r"\s+", "-", doc_id)
    doc_id = re.sub(r"[^\w\-]", "-", doc_id)
    doc_id = re.sub(r"-+", "-", doc_id)
    return doc_id.strip("-").lower()


def resolve_link_path(link_str, current_rel_path):
    """Resolve a link to a vault-relative path, or None if excluded/missing."""
    link_str = urllib.parse.unquote(link_str)

    if not link_str.endswith(".md"):
        link_str += ".md"

    current_dir = os.path.dirname(current_rel_path)

    if link_str.startswith("/"):
        rel = link_str[1:]
    else:
        rel = os.path.normpath(os.path.join(current_dir, link_str))
        rel = rel.replace(os.sep, "/")

    if rel in EXCLUDED_FILES:
        return None

    full = os.path.join(VAULT_PATH, rel)
    return rel if os.path.exists(full) else None
