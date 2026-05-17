# Obsidian GraphRAG — Qdrant Sync & Query

Arsitektur **GraphRAG** untuk knowledge base Obsidian menggunakan **Qdrant** (vector search) + **Gemini Embedding v2** + **graph traversal** antar dokumen.

## Fitur

- **Smart Chunking**: Heading-aware, preserves paragraphs/tables/code blocks, greedy accumulation dengan overlap
- **State Tracking**: JSON-based hash tracking untuk incremental sync (hanya proses file yang berubah)
- **Graph Traversal**: Saat query, tidak hanya similarity search tapi juga menarik dokumen yang saling berelasi
- **Dynamic Relationships**: `linked_doc_ids` dan `backlinked_doc_ids` di-update tanpa re-embed
- **Exclusion Support**: File `index.md` dan `AGENTS.md` di-skip secara otomatis

## Setup

1. Install dependencies:
```bash
cd scripts
pip install -r requirements.txt
```

2. Set environment variable:
```bash
export GEMINI_API_KEY="your-api-key"
```

3. Pastikan Qdrant berjalan di `localhost:6333`.

## Penggunaan

### Sync Semua File ke Qdrant

```bash
python sync.py
```

**Apa yang terjadi:**
- Scan semua `.md` di `knowledge/`, `reference/extracted/`, `logs/`
- Skip file yang tidak berubah (berdasarkan SHA-256 hash)
- Parse frontmatter + extract wiki links
- Chunk dengan strategi heading-aware greedy accumulation
- Embed dengan Gemini v2
- Insert ke collection `test` di Qdrant
- Update relasi antar dokumen (forward + backward links)

### Query dengan Graph Traversal

```bash
python query.py "dampak PHK tekstil terhadap ekonomi"
```

**Flow query:**
1. Embed query dengan Gemini (task_type=`retrieval_query`)
2. Semantic search top 5 chunk paling relevan
3. Traverse graph: kumpulkan `linked_doc_ids` + `backlinked_doc_ids`
4. Fetch chunk dari dokumen terkait (yang mungkin tidak muncul di similarity search)
5. Format jadi konteks utuh untuk LLM

## Struktur File

| File | Fungsi |
|------|--------|
| `config.py` | Konfigurasi path, Qdrant, Gemini, exclusions |
| `markdown_parser.py` | Parse frontmatter YAML, extract markdown/Obsidian links |
| `chunker.py` | Heading-aware chunking dengan greedy accumulation |
| `embedder.py` | Gemini Embedding v2 API wrapper |
| `qdrant_manager.py` | CRUD operations ke Qdrant collection |
| `state_manager.py` | JSON state tracking (hash, chunk count, modified time) |
| `sync.py` | Orchestrator: detect changes → chunk → embed → sync → update relasi |
| `query.py` | GraphRAG retrieval pipeline untuk LLM context |

## State File

`scripts/state.json` menyimpan metadata tiap dokumen:
```json
{
  "knowledge-phk-sepanjang-2025": {
    "relative_path": "knowledge/PHK Sepanjang 2025.md",
    "last_hash": "a3f5c2...",
    "last_chunk_count": 3,
    "last_modified": "2026-05-17T10:00:00"
  }
}
```

## Cara Kerja Update

### File diedit (chunk count berubah)
1. Detect hash berubah
2. `delete_by_doc_id(doc_id)` — hapus SEMUA point lama
3. Re-chunk konten baru
4. Insert point baru
5. Update state

### File baru dengan link ke file lama
1. Insert file baru (linked_doc_ids sementara berisi target)
2. `sync_relationships()` scan SEMUA file
3. Update payload `linked_doc_ids` + `backlinked_doc_ids` untuk affected docs
4. **Tidak ada re-embed**, hanya `set_payload`

## Qdrant Payload Schema

```json
{
  "doc_id": "knowledge-phk-sepanjang-2025",
  "doc_path": "knowledge/PHK Sepanjang 2025.md",
  "chunk_index": 0,
  "total_chunks": 3,
  "heading": "## Analisis Root Cause",
  "heading_level": 2,
  "content": "...",
  "chunk_type": "full_section",
  "part": 1,
  "tags": ["Textile", "Layoffs"],
  "linked_doc_ids": ["knowledge-kerugian-nasabah-bank"],
  "backlinked_doc_ids": ["reference-extracted-news-phk-sritex"],
  "char_count": 7450
}
```

## Notes

- Collection name: `test` (bisa ganti di `config.py` atau env `QDRANT_COLLECTION`)
- Gemini model default: `models/text-embedding-004` (768 dimensi)
- Chunking safety limit: 7500 karakter (margin dari limit 8100)
- Overlap antar chunk: 1 elemen terakhir dibawa ke chunk berikutnya untuk konteks kontinuitas
