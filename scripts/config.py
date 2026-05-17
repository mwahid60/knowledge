"""Configuration for Obsidian GraphRAG with Qdrant."""
import os

from dotenv import load_dotenv

# Load .env from the scripts directory
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT_PATH = BASE_DIR
STATE_FILE = os.path.join(BASE_DIR, "scripts", "state.json")

# Qdrant
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "test")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_USE_HTTPS = os.getenv("QDRANT_USE_HTTPS", "false").lower() in ("true", "1", "yes")
QDRANT_VERIFY_SSL = os.getenv("QDRANT_VERIFY_SSL", "true").lower() in ("true", "1", "yes")

# Gemini Embedding
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "models/text-embedding-004")
GEMINI_MAX_CHARS = 8100  # Gemini embedding v2 limit
SAFE_CHUNK_LIMIT = 7500  # Safety margin below hard limit
VECTOR_SIZE = 768  # Dimensions for text-embedding-004

# Exclusions — these files are NEVER indexed nor linked
EXCLUDED_FILES = {
    "knowledge/index.md",
    "reference/index.md",
    "AGENTS.md",
}

# Glob patterns to scan for markdown files
SCAN_PATTERNS = [
    "knowledge/**/*.md",
    "reference/extracted/**/*.md",
    "logs/**/*.md",
]
