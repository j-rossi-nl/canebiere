import json

from datetime import datetime
from pathlib import Path
from typing import Iterable

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ARTICLES_DIR = ROOT / "data" / "articles"

FIELDS = ["title", "date", "author", "url", "html", "full_text"]

# Les pages par saison commencent avec la saison 2021-2022
FIRST_SEASON_PAGE = "2021-2022"


def date_to_season(date: datetime) -> str:
    # La saison N/N+1 dure du 1er Aout N au 31 Juillet N+1
    if date.month <= 7:
        return f"{date.year - 1}-{date.year}"
    return f"{date.year}-{date.year + 1}"


def season_file(season: str, dir_: Path = ARTICLES_DIR) -> Path:
    return dir_ / f"{season}.jsonl"


def season_pages(dir_: Path = ARTICLES_DIR) -> list[str]:
    """Les saisons qui ont droit à leur page, de la plus ancienne à la plus récente."""
    return sorted(p.stem for p in dir_.glob("*.jsonl") if p.stem >= FIRST_SEASON_PAGE)


def season_page_name(season: str) -> str:
    return season.replace("-", "_")


def iter_articles(dir_: Path = ARTICLES_DIR) -> Iterable[dict]:
    for path in sorted(dir_.glob("*.jsonl")):
        with path.open(encoding="utf-8") as src:
            for line in src:
                if line.strip():
                    yield json.loads(line)


def known_urls(dir_: Path = ARTICLES_DIR) -> set[str]:
    return {article["url"] for article in iter_articles(dir_)}


def write_articles(articles: Iterable[dict], dir_: Path = ARTICLES_DIR) -> list[Path]:
    """Merge articles into the per-season files: dedup by url, sorted by date."""
    by_season: dict[str, dict[str, dict]] = {}
    for article in articles:
        season = date_to_season(datetime.fromisoformat(article["date"]))
        by_season.setdefault(season, {})[article["url"]] = {k: article[k] for k in FIELDS}

    dir_.mkdir(parents=True, exist_ok=True)
    written = []
    for season, new in by_season.items():
        path = season_file(season, dir_)
        merged = {}
        if path.exists():
            with path.open(encoding="utf-8") as src:
                merged = {a["url"]: a for a in map(json.loads, src) if a}
        merged.update(new)
        with path.open("w", encoding="utf-8") as out:
            for article in sorted(merged.values(), key=lambda a: a["date"]):
                out.write(json.dumps(article, ensure_ascii=False) + "\n")
        written.append(path)
    return written


def load_articles(dir_: Path = ARTICLES_DIR) -> pd.DataFrame:
    df = pd.DataFrame(list(iter_articles(dir_)), columns=FIELDS)
    df = df.rename(
        columns={
            "title": "Titre",
            "date": "Date",
            "author": "Auteur",
            "html": "html",
            "full_text": "full_text",
            "url": "url",
        }
    )
    df["Date"] = pd.to_datetime(df["Date"], utc=True).dt.tz_localize(None)
    df["Saison"] = df["Date"].apply(date_to_season)
    return df.sort_values("Date").reset_index(drop=True)
