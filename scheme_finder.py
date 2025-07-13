"""Utility to match user text against schemes CSV."""
from __future__ import annotations
import pandas as pd
import os
import re
from functools import lru_cache

CSV_PATH = os.path.join(os.path.dirname(__file__), "data", "schemes.csv")

@lru_cache(maxsize=1)
def _load_df() -> pd.DataFrame:
    if not os.path.exists(CSV_PATH):
        return pd.DataFrame()
    return pd.read_csv(CSV_PATH)


def find_schemes(user_text: str):
    df = _load_df()
    if df.empty:
        return []

    matches = []
    text_lower = user_text.lower()
    for _, row in df.iterrows():
        keyword = str(row["Keyword"]).lower()
        # simple keyword match
        if re.search(rf"\b{re.escape(keyword)}\b", text_lower):
            matches.append(row)
    # Return top 3
    return matches[:3]
