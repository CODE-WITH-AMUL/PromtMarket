from pathlib import Path

import polars as pl
from django.core.cache import cache
from django.conf import settings


def _get_cache_key(csv_path: Path) -> str:
    mtime = int(csv_path.stat().st_mtime) if csv_path.exists() else 0
    return f"prompt_catalog:{csv_path}:{mtime}"


def _load_rows(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        return []

    key = _get_cache_key(csv_path)
    cached_rows = cache.get(key)
    if cached_rows is not None:
        return cached_rows

    df = pl.read_csv(csv_path)
    if "Domain" in df.columns:
        df = df.rename({"Domain": "domain"})
    if "domain" not in df.columns:
        return []

    rows = df.to_dicts()
    cache.set(key, rows, timeout=settings.CACHE_TTL_SECONDS)
    return rows


def get_prompt_catalog(csv_path: Path, selected_domain: str | None) -> tuple[list[dict], list[str]]:
    rows = _load_rows(csv_path)
    if not rows:
        return [], []

    domains = sorted({row.get("domain") for row in rows if row.get("domain")})

    if selected_domain and selected_domain in domains:
        rows = [row for row in rows if row.get("domain") == selected_domain]

    return rows, domains
