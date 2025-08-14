# utils.py — ortak yardımcılar
from __future__ import annotations

import os
import re
import csv
import time
import json
import threading
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple

import requests

try:
    import streamlit as st
except Exception:  # utils'i test ederken Streamlit yoksa sorun olmasın
    class _Dummy:
        secrets = {}
    st = _Dummy()  # type: ignore


# -----------------------------
# Secrets / Config helpers
# -----------------------------
def get_secret(name: str, default: str = "") -> str:
    """
    Önce st.secrets[name], yoksa os.environ[name], yoksa default.
    """
    try:
        if hasattr(st, "secrets") and name in getattr(st, "secrets", {}):
            return str(st.secrets[name])
    except Exception:
        pass
    return os.getenv(name, default)


# -----------------------------
# Rate limit (nazik bekletme)
# -----------------------------
class RateLimiter:
    """
    Ardışık çağrılar arasında min_interval saniye bekler.
    Thread-safe.
    """
    def __init__(self, min_interval: float = 0.6):
        self.min_interval = float(min_interval)
        self._last = 0.0
        self._lock = threading.Lock()

    def wait(self) -> None:
        with self._lock:
            now = time.monotonic()
            delta = now - self._last
            if delta < self.min_interval:
                time.sleep(self.min_interval - delta)
            self._last = time.monotonic()


# -----------------------------
# HTTP helpers (retry'li GET)
# -----------------------------
def http_get_retry(
    url: str,
    params: Mapping[str, Any],
    headers: Optional[Mapping[str, str]] = None,
    timeout: int = 30,
    retries: int = 2,
    backoff: float = 0.8,
    ratelimiter: Optional[RateLimiter] = None,
) -> Dict[str, Any]:
    """
    Küçük ölçekli projeler için pratik GET:
    - nazik rate-limit
    - 429/5xx durumlarında kısa retry (exponential backoff)
    """
    if ratelimiter:
        ratelimiter.wait()

    h = {"User-Agent": "yourwayally/1.0 (+contact@example.com)"}
    if headers:
        h.update(headers)

    attempt = 0
    while True:
        attempt += 1
        try:
            r = requests.get(url, params=params, headers=h, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else 0
            # 429 ve 5xx için retry
            if attempt <= retries and (status == 429 or 500 <= status < 600):
                time.sleep(backoff * attempt)
                continue
            raise
        except Exception:
            if attempt <= retries:
                time.sleep(backoff * attempt)
                continue
            raise


# -----------------------------
# Basit TTL cache (in-memory)
# -----------------------------
class TTLCache:
    """
    Aşırı basit JSON-uyumlu TTL cache (process içi).
    Not: Streamlit @st.cache_data zaten var; bu cache modül dışı kullanım içindir.
    """
    def __init__(self, ttl_sec: int = 1800, max_items: int = 512):
        self.ttl = ttl_sec
        self.max_items = max_items
        self._store: Dict[str, Tuple[float, Any]] = {}
        self._lock = threading.Lock()

    def _prune(self) -> None:
        now = time.time()
        keys = [k for k, (ts, _) in self._store.items() if now - ts > self.ttl]
        for k in keys:
            self._store.pop(k, None)
        # çok büyürse FIFO tarzı buda
        if len(self._store) > self.max_items:
            for k in list(self._store.keys())[: len(self._store) - self.max_items]:
                self._store.pop(k, None)

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            self._prune()
            item = self._store.get(key)
            if not item:
                return None
            ts, val = item
            if time.time() - ts > self.ttl:
                self._store.pop(key, None)
                return None
            return val

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._prune()
            self._store[key] = (time.time(), value)


# -----------------------------
# Metin yardımcıları
# -----------------------------
_LATLON_RE = re.compile(r"(-?\d{1,2}\.\d+)[ ,]+(-?\d{1,3}\.\d+)")

def extract_latlon(text: str) -> Optional[Tuple[float, float]]:
    """
    '38.42, 27.14' gibi metinden (lat, lon) döndürür.
    """
    m = _LATLON_RE.search(text or "")
    if not m:
        return None
    try:
        return float(m.group(1)), float(m.group(2))
    except Exception:
        return None

def bullets(lines: Iterable[str]) -> str:
    """
    Listeyi markdown bullet olarak birleştirir.
    """
    cleaned = [f"• {l.strip()}" for l in lines if str(l).strip()]
    return "\n".join(cleaned)

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


# -----------------------------
# Basit CSV log
# -----------------------------
def append_csv(path: str, row: Mapping[str, Any]) -> None:
    """
    path: 'logs/usage.csv' gibi. Yoksa dosya+klasör oluşturur.
    row: {"ts": ..., "event": ..., "value": ...}
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    file_exists = os.path.exists(path)

    with open(path, "a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(row.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)


# -----------------------------
# Küçük yardımcı hesaplar (opsiyonel)
# -----------------------------
def safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return default

def normalize_query(q: str) -> str:
    return " ".join((q or "").strip().split())
