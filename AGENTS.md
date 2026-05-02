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
│   │   ├── academic/            # Extracted information from academic research
│   │   ├── information/         # Extracted non-news information or general information
│   │   └── news/                # Individual news case files
│   └── raw/                     # Raw PDFs and documents
├── .obsidian/                   # Obsidian configuration (gitignored)
└── .venv/                       # Python virtual environment (gitignored)
```

## Research Workflow
When user ask you to starting a research about specific topic, use this workflow:
1. **Check Reference Index First** - Read `reference/index.md` to check if the topic already exists in the extracted folders (academic, information, or news). If the information is already available, use the existing reference files instead of searching the web.
2. **Search Existing References** - If the topic exists in the index, read the relevant reference files to gather information.
3. **Web Search (if needed)** - Only perform web search if the topic is not found in the reference index or if the existing information is insufficient.
4. **Create New Reference Files** - After gathering new information, create appropriate reference files following the naming conventions and update `reference/index.md` with the new entries.

### Academic Reference Format
For academic papers, use **numbered list format** for the reference section:
```markdown
## Daftar Pustaka

1. Author, A. A., & Author, B. B. (Year). Title of the article. *Journal Name*, volume(issue), pages. https://doi.org/xxxxx
2. Author, C. C. (Year). Title of the book. Publisher.
```
- Use `## Daftar Pustaka` as the section heading
- Number each reference sequentially
- Use italic (`*text*`) for journal names and book titles
- Include DOI or URL when available

## File Naming Conventions

### Knowledge Files
- Use descriptive names in Indonesian
- Format: `<Topic>.md`
- Example: `Pelanggaran Hukum Aparat Negara.md`

### Logs Files
- a file that writes about everything that has been done that day
- Format: `YYYY-MM-DD.md`
- Example: `2026-04-23.md`

### Reference Files

#### News & Information
- Format: `<subject>-<brief-description>-<location>-<YYYY-MM>.md`
- Use lowercase with hyphens
- Include date for filename in news/ and exclude date for information/
- Example: `tni-al-tembak-bos-rental-banten-2025-01.md`

#### Academic Research
- Format: `<Academic Title in The File>.md`
- Use capital word
- Information is extracted from academic paper
- Example: `Hierarchical Reasoning Model.md`

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
- Order tags for news: Subject → Location → Category → Descriptive tags → Descriptive tags
- Example tags for news:
	- Bank_DKI
	- Jakarta
	- Hacking
	- BI-FAST
	- Hacker_Syndicate
- Location = province name (not city), or "Nasional" for national cases
- Order tags for Academic : Main Category → Sub Category → Descriptive tags → Descriptive tags → Descriptive tags
- Example for Academic:
	- Psychology
	- Social_Behavior
	- Personality
	- Dark_Personality
	- Antisocial_Behavior
- **CRITICAL: ALL tags MUST be written in English EXCEPT location and subject**
  - Location tags: Use Indonesian province names or "Nasional"
  - Subject tags: Use Indonesian company/institution names
  - All other tags (Category, Descriptive): MUST be in English
  - Examples of CORRECT tags:
    - Subject: Sritex, Bank_DKI, eFishery
    - Location: Jawa_Tengah, Jakarta, Nasional
    - Category: Textile, Banking, Startup, Manufacturing
    - Descriptive: Layoffs, Bankruptcy, Fraud, Hacking
  - Examples of INCORRECT tags:
    - ❌ Tekstil, PHK, Pailit, Keuangan (must be: Textile, Layoffs, Bankruptcy, Finance)
    - ❌ Berita, Hukum (must be: News, Law)

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

### Information Files (Company Profiles / General Information)
Files in `reference/extracted/information/` follow a standardized company profile format. Use this structure for all new information files:

**Standard Sections (in order):**
1. **Ringkasan** — Overview paragraph + attribute table (Nama resmi, Kode emiten, Industri, Didirikan, Kantor pusat, Wilayah operasi, Situs web, dll.)
2. **Sejarah Berdiri** — Chronological history with era subsections (e.g., Awal Mula, Era Pertumbuhan, Transformasi, Era Modern)
3. **Kinerja Keuangan** — Table with latest financial metrics (Pendapatan, Laba bersih, Total aset, Total ekuitas, Karyawan)
4. **Kepemilikan Saham** — Shareholder tables (Pemegang Saham Utama + Riwayat Kepemilikan)
5. **Kepemimpinan Perusahaan** — Board of Directors / Commissioners tables (Terkini + Riwayat)
6. **Profil Direksi/Komisaris** (optional) — Detailed career history of key leaders
7. **Industri & Bidang Usaha** — Numbered list of business segments
8. **Produk & Layanan** — Categorized tables of products/services
9. **Afiliasi & Anak Usaha** — Subsidiary/affiliate tables
10. **Fakta Menarik Tambahan** — Numbered list of unique/interesting facts (8–10 items)
11. **Referensi** — Numbered list of sources + Tavily Search citations

**Formatting Rules:**
- Use `---` horizontal rules to separate major sections
- Use markdown tables for simple data, HTML tables only when complex formatting needed
- Include financial data with year label (e.g., "Kinerja Keuangan (2023)")
- Tag Tavily-sourced references with `**Tavily Search**: "Title" — Source`
- Language: Indonesian (Bahasa Indonesia), except English terms for official names
- File naming: `<Company Name>.md` (no date, Title Case, e.g., `Panca Global Sekuritas.md`)

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

## Analysis Guidelines

### Root Cause Analysis (RCA)
Setiap analisis kasus HARUS menjelaskan **sebab dan akibat** secara komprehensif:

1. **Identifikasi Root Cause**: Jangan hanya menyebut faktor (misal: "perang dagang"), tapi jelaskan **mekanisme** kenapa faktor tersebut menyebabkan masalah
   - ❌ Buruk: "Perang dagang AS-China menyebabkan PHK"
   - ✅ Baik: "Tarif impor 145% oleh AS terhadap produk China (Mei 2025) memaksa eksportir China mencari pasar alternatif. China melakukan dumping produk tekstil ke Indonesia dengan harga 30-40% di bawah harga pasar. Produk impor ini membanjiri pasar domestik, menyebabkan penurunan permintaan lokal 25%. Perusahaan tekstil lokal kehilangan pendapatan, tidak mampu membayar utang, dan akhirnya bangkrut → PHK massal"

2. **Chain of Effects**: Jelaskan rantai dampak secara berurutan:
   - **Trigger** (pemicu) → **Direct Effect** (dampak langsung) → **Indirect Effect** (dampak tidak langsung) → **Final Impact** (dampak akhir)
   - Contoh: Kenaikan suku bunga The Fed 5,5% → arus modal keluar dari emerging markets → pelemahan rupiah 12% → biaya impor bahan baku naik → biaya produksi naik 18% → harga jual tidak kompetitif → penurunan order 30% → PHK

3. **Multiple Perspectives**: Analisis harus mencakup:
   - **Faktor Eksternal**: Geopolitik, ekonomi global, kebijakan negara lain
   - **Faktor Internal**: Manajemen, kebijakan perusahaan, teknologi
   - **Faktor Struktural**: Regulasi, infrastruktur, rantai pasok

4. **Quantitative Impact**: Sertakan angka dan persentase jika tersedia untuk mengukur dampak

### Standard Analysis Sections

Include these standard analyses when relevant:
1. **Pola Temporal** - Temporal patterns with quarterly breakdown
2. **Modus Dominan** - Dominant modus operandi with specific examples
3. **Root Cause & Effect Chain** - Sebab-akibat komprehensif (WAJIB)
4. **Pola Impunitas** - Impunity patterns
5. **Kesesuaian Hukuman** - Analysis of punishment vs law
6. **Data Konteks** - Context from NGOs/Human rights orgs
7. **Rekomendasi** - Specific, actionable recommendations

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
