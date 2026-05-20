"""API client helpers for arXiv and Semantic Scholar.

All HTTP requests go through ``_get`` which adds a descriptive User-Agent
header and retries with exponential back-off on transient failures.

Response normalisers return a uniform candidate dict understood by the rest
of the pipeline:

    {
        "arxiv_id":  str | None,
        "title":     str,
        "authors":   list[str],
        "year":      int | None,
        "abstract":  str,
        "venue":     str,
        "citations": int,
        "links": {
            "arxiv": str | None,
            "pdf":   str | None,
            "doi":   str | None,
        },
    }

Isolating all API I/O here means future schema drift is a one-file fix.
"""

from __future__ import annotations

import logging
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

USER_AGENT = (
    "awesome-radio-map-estimation/1.0 "
    "(+https://github.com/DongYang26/awesome-radio-map-estimation)"
)

ARXIV_BASE = "https://export.arxiv.org/api/query"
S2_PAPER_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"
S2_PAPER_FIELDS = (
    "externalIds,title,authors,year,venue,abstract,citationCount,openAccessPdf"
)

# Default retry parameters
_DEFAULT_RETRIES = 3
_DEFAULT_BACKOFF_BASE = 2.0   # seconds; doubles each attempt
_DEFAULT_TIMEOUT = 30          # seconds per request


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _get(
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    retries: int = _DEFAULT_RETRIES,
    backoff_base: float = _DEFAULT_BACKOFF_BASE,
    timeout: int = _DEFAULT_TIMEOUT,
    s2_api_key: str | None = None,
) -> requests.Response:
    """GET *url* with retry + exponential back-off.

    On a transient failure (connection error, 429, 5xx) the request is
    retried up to *retries* times with a sleep of
    ``backoff_base * 2 ** attempt`` seconds.

    Raises ``requests.HTTPError`` after all retries are exhausted.
    """
    merged_headers: dict[str, str] = {"User-Agent": USER_AGENT}
    if headers:
        merged_headers.update(headers)
    if s2_api_key:
        merged_headers["x-api-key"] = s2_api_key

    last_exc: Exception | None = None
    for attempt in range(retries + 1):
        if attempt:
            sleep_s = backoff_base * (2 ** (attempt - 1))
            logger.debug("Retry %d/%d after %.1fs (url=%s)", attempt, retries, sleep_s, url)
            time.sleep(sleep_s)
        try:
            resp = requests.get(
                url,
                params=params,
                headers=merged_headers,
                timeout=timeout,
            )
            if resp.status_code in (429, 500, 502, 503, 504):
                logger.warning(
                    "HTTP %d from %s (attempt %d/%d)",
                    resp.status_code, url, attempt + 1, retries + 1,
                )
                last_exc = requests.HTTPError(response=resp)
                continue
            resp.raise_for_status()
            return resp
        except requests.ConnectionError as exc:
            logger.warning("Connection error: %s (attempt %d/%d)", exc, attempt + 1, retries + 1)
            last_exc = exc
        except requests.Timeout as exc:
            logger.warning("Timeout: %s (attempt %d/%d)", exc, attempt + 1, retries + 1)
            last_exc = exc

    raise requests.RequestException(
        f"All {retries + 1} attempts failed for {url}"
    ) from last_exc


# ---------------------------------------------------------------------------
# arXiv helpers
# ---------------------------------------------------------------------------

def _parse_arxiv_id(entry: Any) -> str | None:
    """Extract the bare arXiv id from a feedparser entry (e.g. '2210.12345v2' -> '2210.12345')."""
    raw = getattr(entry, "id", None) or ""
    # feedparser sets entry.id to the full URL like https://arxiv.org/abs/2210.12345v2
    parts = raw.rstrip("/").split("/")
    aid = parts[-1] if parts else ""
    # Strip version suffix vN
    if aid and "v" in aid:
        aid = aid.rsplit("v", 1)[0]
    return aid or None


def normalise_arxiv_entry(entry: Any) -> dict:
    """Normalise one feedparser entry into the pipeline candidate dict."""
    arxiv_id = _parse_arxiv_id(entry)
    authors = [
        (a.get("name") or "").strip()
        for a in getattr(entry, "authors", [])
        if isinstance(a, dict)
    ]
    # published: '2022-10-21T17:59:04Z'
    published = getattr(entry, "published", "") or ""
    year: int | None = None
    if published and len(published) >= 4:
        try:
            year = int(published[:4])
        except ValueError:
            pass

    title = (getattr(entry, "title", "") or "").strip().replace("\n", " ")
    abstract = (getattr(entry, "summary", "") or "").strip().replace("\n", " ")

    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}" if arxiv_id else None

    doi: str | None = None
    for link in getattr(entry, "links", []):
        if isinstance(link, dict) and link.get("type") == "text/html":
            href = link.get("href", "")
            if "doi.org" in href:
                doi = href
                break

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "year": year,
        "abstract": abstract,
        "venue": "",
        "citations": 0,
        "links": {
            "arxiv": arxiv_url,
            "pdf": pdf_url,
            "doi": doi,
        },
        "_source": "arxiv",
    }


def fetch_arxiv(
    query: str,
    max_results: int = 50,
    days: int | None = None,
    rate_limit_sleep: float = 3.0,
) -> list[dict]:
    """Search arXiv and return a list of normalised candidate dicts.

    Args:
        query:           arXiv search query string (will be wrapped in
                         ``all:`` if no field prefix is given).
        max_results:     Maximum papers returned per query.
        days:            If provided, filter to papers submitted within the
                         last *days* days (using arXiv's ``submittedDate``
                         field).
        rate_limit_sleep: Seconds to sleep after the request (arXiv
                         requests 3 s between calls).
    """
    try:
        import feedparser  # type: ignore
    except ImportError as exc:
        raise ImportError(
            "feedparser is required: pip install feedparser"
        ) from exc

    search_query = query
    if days is not None:
        from datetime import datetime, timedelta, timezone
        cutoff = datetime.now(tz=timezone.utc) - timedelta(days=days)
        date_str = cutoff.strftime("%Y%m%d%H%M%S")
        search_query = f"({query}) AND submittedDate:[{date_str} TO 99991231235959]"

    params = {
        "search_query": search_query,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    logger.info("arXiv query: %s", search_query)
    try:
        resp = _get(ARXIV_BASE, params=params)
    except requests.RequestException as exc:
        logger.error("arXiv fetch failed: %s", exc)
        return []
    finally:
        time.sleep(rate_limit_sleep)

    feed = feedparser.parse(resp.text)
    candidates = [normalise_arxiv_entry(e) for e in feed.get("entries", [])]
    logger.info("arXiv returned %d entries", len(candidates))
    return candidates


# ---------------------------------------------------------------------------
# Semantic Scholar helpers
# ---------------------------------------------------------------------------

def normalise_s2_paper(paper: dict) -> dict:
    """Normalise one Semantic Scholar paper dict into the pipeline candidate dict."""
    external = paper.get("externalIds") or {}
    arxiv_id: str | None = external.get("ArXiv") or external.get("arxiv") or None

    authors = [
        (a.get("name") or "").strip()
        for a in (paper.get("authors") or [])
        if isinstance(a, dict)
    ]

    year: int | None = paper.get("year")
    if isinstance(year, float):
        year = int(year)

    doi: str | None = external.get("DOI") or None

    oap = paper.get("openAccessPdf") or {}
    pdf_url: str | None = oap.get("url") if isinstance(oap, dict) else None
    arxiv_url = f"https://arxiv.org/abs/{arxiv_id}" if arxiv_id else None

    title = (paper.get("title") or "").strip()
    abstract = (paper.get("abstract") or "").strip()
    venue = (paper.get("venue") or "").strip()
    citations = paper.get("citationCount") or 0
    if not isinstance(citations, int):
        citations = 0

    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "year": year,
        "abstract": abstract,
        "venue": venue,
        "citations": citations,
        "links": {
            "arxiv": arxiv_url,
            "pdf": pdf_url,
            "doi": doi,
        },
        "_source": "semantic-scholar",
        "_s2_paper_id": paper.get("paperId"),
    }


def fetch_s2(
    query: str,
    limit: int = 50,
    rate_limit_sleep: float = 1.0,
    s2_api_key: str | None = None,
) -> list[dict]:
    """Search Semantic Scholar and return a list of normalised candidate dicts.

    Args:
        query:            Free-text search query.
        limit:            Maximum papers returned (S2 cap is 100 per request).
        rate_limit_sleep: Seconds to sleep after the request (S2 unauthenticated
                          rate limit is tight — 1 req/s is safe).
        s2_api_key:       Optional S2 API key for higher rate limits.
    """
    params: dict[str, Any] = {
        "query": query,
        "limit": min(limit, 100),
        "fields": S2_PAPER_FIELDS,
    }

    logger.info("S2 query: %s", query)
    try:
        resp = _get(S2_PAPER_SEARCH, params=params, s2_api_key=s2_api_key)
    except requests.RequestException as exc:
        logger.error("Semantic Scholar fetch failed: %s", exc)
        return []
    finally:
        time.sleep(rate_limit_sleep)

    data = resp.json()
    raw_papers = data.get("data") or []
    candidates = [normalise_s2_paper(p) for p in raw_papers if isinstance(p, dict)]
    logger.info("S2 returned %d papers", len(candidates))
    return candidates
