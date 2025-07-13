"""Simple JSONL store for call logs and issues."""
import json
import os
from datetime import datetime
from typing import List, Dict

STORE_FILE = os.path.join(os.path.dirname(__file__), "data", "call_logs.jsonl")

def log_call(entry: Dict):
    entry["timestamp"] = datetime.utcnow().isoformat()
    with open(STORE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def get_last_calls(limit: int = 100) -> List[Dict]:
    if not os.path.exists(STORE_FILE):
        return []
    lines = []
    with open(STORE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()[-limit:]
    return [json.loads(l) for l in lines]
