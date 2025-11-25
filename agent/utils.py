import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    t = text.strip()
    t = re.sub(r"\s+", " ", t)
    return t

def ensure_min_length(text: str, min_len: int = 10):
    if not text or len(text.strip()) < min_len:
        raise ValueError("Please provide a clear complaint with location/context (min 10 characters).")
