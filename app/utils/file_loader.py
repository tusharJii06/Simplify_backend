from pathlib import Path

def read_text_file(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    return p.read_text(encoding="utf-8")