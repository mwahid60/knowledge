# AGENTS.md

This is an Obsidian-based knowledge repository for documenting news and research. This file provides guidelines for agentic coding assistants working in this codebase.

## Repository Structure

```
/Users/mwahid2004/Library/CloudStorage/OneDrive-Personal/Notes/Knowledge/
├── knowledge/                    # Main knowledge files (synthesized analysis)
│   ├── Pelanggaran Hukum Aparat Negara Sepanjang 2025.md
│   └── Kerugian Nasabah Bank Sepanjang 2025.md
├── logs/                        # Main folder to store logs
├── reference/
│   ├── extracted/
│   │   └── academic/            # Extracted information from academic research
│   │   ├── information/         # Extracted non-news information or general information
│   │   └── news/                # Individual news case files
│   └── raw/                     # Raw PDFs and documents
├── .obsidian/                   # Obsidian configuration (gitignored)
└── .venv/                       # Python virtual environment (gitignored)
```

## File Naming Conventions

### Knowledge Files
- Use descriptive names in Indonesian
- Format: `<Topic>.md`
- Example: `Pelanggaran Hukum Aparat Negara.md`

### Logs Files
- a file that writes about everything that has been done that day
- Format: `YYYY-MM-DD.md`
- Example: `2026-04-23.md

### Reference Files

#### News & Information
- Format: `<subject>-<brief-description>-<location>-<YYYY-MM>.md`
- Use lowercase with hyphens
- Include date for filename in news/ and exclude date for information/
- Example: `tni-al-tembak-bos-rental-banten-2025-01.md`

#### 

## Front Matter Standards

### Knowledge Files
```yaml
---
created_at: YYYY-MM-DD
tags:
  - Tag1
  - Tag2
  - Tag_With_Spaces
reference:
  - "[[filename-without-extension]]"
---
```

### Reference Files
```yaml
---
date: YYYY-MM-DD
published_by:
  - Source 1
  - Source 2
url:
  - https://example.com/article1
  - https://example.com/article2
tags:
  - Subject
  - Location
  - Category
  - Tag_4
  - Tag_5
---
```

**Tag Rules:**
- Exactly 5 tags for reference files
- Use Title_Case with underscores for multi-word tags
- Order: Institution → Location → Category → Descriptive tags
- Location = province name (not city), or "Nasional" for national cases

## Content Guidelines

### Knowledge Files (Main Analysis)
- Use HTML tables for main data (supports rowspan and complex formatting)
- Include YAML front matter with tags and references
- Structure: Overview → Main Table → Summary Tables → Analysis → Methodology
- Use wikilinks `[[filename]]` for internal references
- External links in HTML: `<a href="URL">Title</a>`

### Reference Files (Individual Cases)
- Standard sections: Ringkasan → Detail Kasus → Perkembangan Hukum → Respons Institusi → Analisis Konteks
- Include complete URLs in front matter
- Use bullet points for key facts
- Quote relevant passages from sources

## Table Formatting

### Main Tables (HTML)
```html
<table>
<thead>
<tr>
  <th width="8%">Column1</th>
  <th width="10%">Column2</th>
  <!-- Use width attributes for column sizing -->
</tr>
</thead>
<tbody>
<tr>
  <td>Data</td>
  <td>Data</td>
</tr>
</tbody>
</table>
```

### Summary Tables (Markdown)
Use standard markdown tables for simple summaries:
```markdown
| Kategori | Count |
|----------|-------|
| Category | 5     |
```

## Writing Style

- **Language**: Indonesian (Bahasa Indonesia)
- **Tone**: Objective, factual, analytical
- **Citations**: Always cite sources with URLs
- **Dates**: Use DD Month YYYY format in content
- **Numbers**: Use thousand separators (e.g., Rp 2,65 miliar)

## Analysis Sections

Include these standard analyses when relevant:
1. **Pola Temporal** - Temporal patterns
2. **Modus Dominan** - Dominant modus operandi
3. **Pola Impunitas** - Impunity patterns
4. **Kesesuaian Hukuman** - Analysis of punishment vs law
5. **Data Konteks** - Context from NGOs/Human rights orgs
6. **Rekomendasi** - Recommendations

## Git Workflow

- Do NOT commit unless explicitly asked by user
- Check git status before making changes
- Never commit secrets or credentials
- Use descriptive commit messages when asked to commit

## Code Style Guidelines

This is a Markdown-based knowledge repository, not a software project. There are no build, lint, or test commands. Follow these content formatting standards:

- **No comments** in Markdown files unless explicitly requested
- **Consistent indentation**: 2 spaces for nested list items, 4 spaces for code blocks
- **Line breaks**: Use blank lines between sections and paragraphs
- **Headings**: Use `##` for main sections, `###` for subsections, `####` for minor sections
- **Lists**: Use `-` for unordered lists, `1.` for ordered lists
- **Bold/italic**: Use `**bold**` for emphasis, `*italic*` for citations or foreign terms
- **Quotes**: Use `>` for blockquotes from sources
- **Code blocks**: Use triple backticks with language identifier when needed
- **Horizontal rules**: Use `---` to separate major sections

## Error Handling & Verification

- Always verify facts with at least 2 independent sources before adding
- Use Tavily search for URL verification
- Cross-reference dates, names, and numbers across multiple news outlets
- Mark uncertain information with "diduga" or "belum dikonfirmasi"
- Never fabricate or guess URLs, dates, or facts

## Prohibited Actions

- Never create/modify files in `.obsidian/` or `.venv/`
- Never delete `.gitignore` entries
- Never guess URLs - only use verified URLs from search
- Never create placeholder content
- Never modify files without reading them first

## Obsidian Integration

This repo is designed for Obsidian:
- Wikilinks `[[filename]]` connect related notes
- Tags enable graph view navigation
- HTML tables render properly in Obsidian
- YAML front matter enables dataview queries
