import json, time, os
from typing import Dict, Any, List

MEMORY_PATH = os.environ.get("CIVICASSIST_MEMORY_PATH", "agent/memory.json")

def _read_memory_raw() -> List[Dict[str,Any]]:
    try:
        with open(MEMORY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _write_memory_raw(data: List[Dict[str,Any]]):
    os.makedirs(os.path.dirname(MEMORY_PATH), exist_ok=True)
    with open(MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def generate_id() -> str:
    return f"CMP-{time.strftime('%Y%m%d-%H%M%S')}"

def log_interaction(record: Dict[str,Any]):
    memory = _read_memory_raw()
    memory.append(record)
    _write_memory_raw(memory)

def get_status(complaint_id: str) -> str:
    for rec in _read_memory_raw():
        if rec.get("id") == complaint_id:
            return rec.get("status","Unknown")
    return "Not found"

def update_status(complaint_id: str, new_status: str) -> bool:
    memory = _read_memory_raw()
    changed = False
    for rec in memory:
        if rec.get("id") == complaint_id:
            rec["status"] = new_status
            changed = True
            break
    if changed:
        _write_memory_raw(memory)
    return changed

def count_similar(text: str, category: str) -> int:
    t = text.lower()
    return sum(1 for rec in _read_memory_raw()
               if rec.get("category") == category and t in rec.get("text","").lower())
