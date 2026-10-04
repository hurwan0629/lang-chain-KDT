from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
SOURCES_CSV = DATA_DIR / "sources.csv"
VIDEO_CUA_DIR = DATA_DIR / "videocua"
VIDEO_CUA_INDEX = VIDEO_CUA_DIR / "tasks.csv"
PIE2F_DIR = DATA_DIR / "PIE2F"
PIE2F_INDEX_DIR = PIE2F_DIR / "indexes"
PIE2F_PROCESSED_DIR = DATA_DIR / "pie2f_processed"
CHECKPOINT_DIR = PROJECT_DIR / "checkpoints"
DEFAULT_CHECKPOINT = CHECKPOINT_DIR / "activity_gru.pt"

CLIP_MODEL_NAME = "openai/clip-vit-base-patch32"

ACTIVITY_PROMPTS = {
    "gaming": "a computer screen showing a video game being played",
    "entertainment_video": "a computer screen showing an entertaining video being watched",
    "educational_video": "a computer screen showing an educational video or lecture being watched",
    "python_coding": "a computer screen showing Python code being written or debugged",
    "java_coding": "a computer screen showing Java code being written or debugged",
    "email": "a computer screen showing emails being read or written",
    "documentation": "a computer screen showing technical documentation or a document being written",
    "reading": "a computer screen showing a book, ebook, paper, or PDF being read",
}

WEAK_LABEL_KEYWORDS = {
    "python_coding": [
        "python", "pytorch", "django", "flask", "pandas", "numpy", "jupyter",
    ],
    "java_coding": [
        "java", "spring boot", "spring framework", "gradle", "maven",
    ],
    "email": [
        "email", "e-mail", "gmail", "outlook", "mailbox", "inbox",
    ],
    "documentation": [
        "documentation", "docs", "readme", "markdown", "word document",
        "technical writing", "report writing",
    ],
    "reading": [
        "ebook", "e-book", "book reading", "paper reading", "pdf reading",
        "research paper",
    ],
    "gaming": [
        "gameplay", "gaming", "playthrough", "walkthrough", "speedrun",
    ],
    "entertainment_video": [
        "vlog", "music video", "trailer", "comedy", "entertainment",
        "reaction video",
    ],
    "educational_video": [
        "tutorial", "lecture", "course", "lesson", "class", "how to",
        "explained", "education",
    ],
}
