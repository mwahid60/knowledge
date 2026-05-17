"""Heading-aware chunking that preserves paragraphs, tables, and code blocks."""
import re

from config import GEMINI_MAX_CHARS, SAFE_CHUNK_LIMIT


def parse_elements(content):
    """Split markdown into atomic (non-splittable) elements."""
    elements = []
    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Code block
        if stripped.startswith("```"):
            block = [line]
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            if i < len(lines):
                block.append(lines[i])
                i += 1
            elements.append(("\n".join(block), "code"))
            continue

        # Table
        if "|" in line:
            block = [line]
            i += 1
            while i < len(lines) and "|" in lines[i]:
                block.append(lines[i])
                i += 1
            elements.append(("\n".join(block), "table"))
            continue

        # Horizontal rule
        if stripped == "---":
            elements.append((line, "hr"))
            i += 1
            continue

        # Heading
        if stripped.startswith("#"):
            elements.append((line, "heading"))
            i += 1
            continue

        # List block
        if re.match(r"^\s*[-*+]\s", line) or re.match(r"^\s*\d+\.\s", line):
            block = [line]
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if nxt.strip() == "":
                    # Peek ahead: continue if next non-empty is indented/list
                    j = i + 1
                    while j < len(lines) and lines[j].strip() == "":
                        j += 1
                    if j < len(lines) and (
                        lines[j].startswith(" ")
                        or re.match(r"^\s*[-*+]\s", lines[j])
                        or re.match(r"^\s*\d+\.\s", lines[j])
                    ):
                        block.append(nxt)
                        i += 1
                        continue
                    break
                if nxt.startswith(" ") or re.match(r"^\s*[-*+]\s", nxt) or re.match(r"^\s*\d+\.\s", nxt):
                    block.append(nxt)
                    i += 1
                else:
                    break
            elements.append(("\n".join(block), "list"))
            continue

        # Empty line
        if stripped == "":
            i += 1
            continue

        # Paragraph
        block = [line]
        i += 1
        while i < len(lines):
            nxt = lines[i]
            if nxt.strip() == "" or nxt.strip().startswith("#") or nxt.strip().startswith("```") or "|" in nxt or re.match(r"^\s*[-*+]\s", nxt) or re.match(r"^\s*\d+\.\s", nxt):
                break
            block.append(nxt)
            i += 1
        elements.append(("\n".join(block), "paragraph"))

    return elements


def group_by_sections(elements):
    """Group elements under their nearest heading."""
    sections = []
    current = {"heading": "", "heading_level": 0, "elements": []}

    for text, etype in elements:
        if etype == "heading":
            if current["elements"] or current["heading"]:
                sections.append(current)
            level = len(text) - len(text.lstrip("#"))
            current = {"heading": text.strip(), "heading_level": level, "elements": []}
        else:
            current["elements"].append((text, etype))

    if current["elements"] or current["heading"]:
        sections.append(current)

    return sections


def greedy_chunk_elements(elements, max_chars):
    """Greedy accumulation with 1-element overlap between chunks."""
    chunks = []
    current = []
    current_len = 0

    for idx, (text, _etype) in enumerate(elements):
        text_len = len(text)

        if text_len > max_chars:
            if current:
                chunks.append("\n\n".join(t for t, _ in current))
                current = []
                current_len = 0
            chunks.append(text[:max_chars])
            continue

        add_len = text_len if not current else text_len + 2  # \n\n separator

        if current_len + add_len > max_chars:
            # Flush current
            chunks.append("\n\n".join(t for t, _ in current))

            # Overlap: carry last element forward for context continuity
            if current:
                last_text, _ = current[-1]
                current = [(last_text, "overlap"), (text, _etype)]
                current_len = len(last_text) + 2 + text_len
            else:
                current = [(text, _etype)]
                current_len = text_len
        else:
            current.append((text, _etype))
            current_len += add_len

    if current:
        chunks.append("\n\n".join(t for t, _ in current))

    return chunks


def chunk_markdown(content, max_chars=SAFE_CHUNK_LIMIT):
    """Main entry: heading-aware chunking with greedy element accumulation."""
    stripped = content.strip()
    if not stripped:
        return []

    # Entire document fits in one chunk
    if len(stripped) <= GEMINI_MAX_CHARS:
        return [{
            "heading": "",
            "heading_level": 0,
            "content": stripped,
            "type": "full_document",
            "part": 1,
        }]

    elements = parse_elements(stripped)
    sections = group_by_sections(elements)
    chunks = []

    for section in sections:
        heading = section["heading"]
        heading_level = section["heading_level"]
        sec_elements = section["elements"]

        if not sec_elements:
            continue

        # Build section text to check size
        sec_text = (heading + "\n\n") if heading else ""
        sec_text += "\n\n".join(t for t, _ in sec_elements)

        if len(sec_text) <= max_chars:
            chunks.append({
                "heading": heading,
                "heading_level": heading_level,
                "content": sec_text.strip(),
                "type": "full_section",
                "part": 1,
            })
        else:
            # Split section with greedy accumulation
            available = max_chars - (len(heading) + 2) if heading else max_chars
            available = max(available, 1000)  # sanity floor
            sub_chunks = greedy_chunk_elements(sec_elements, available)

            for i, sub in enumerate(sub_chunks):
                content_str = f"{heading} (bagian {i + 1})\n\n{sub}" if heading else sub
                chunks.append({
                    "heading": heading,
                    "heading_level": heading_level,
                    "content": content_str,
                    "type": "partial_section",
                    "part": i + 1,
                })

    return chunks
