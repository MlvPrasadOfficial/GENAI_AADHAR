"""LRU embedding cache — avoids re-processing the same image.

Caches FaceResult objects keyed by a SHA-256 hash of the raw image bytes.
When the same Aadhaar card is compared against multiple selfies (or vice
versa), the detection + alignment + embedding step is skipped entirely.

Thread-safe via a simple lock around the LRU dict.
"""

import hashlib
import logging
import threading
from collections import OrderedDict

logger = logging.getLogger(__name__)


class EmbeddingCache:
    """LRU cache for FaceResult objects, keyed by image content hash.

    Usage:
        cache = EmbeddingCache(max_size=64)
        key = cache.hash_key(image_bytes)
        hit = cache.get(key)
        if hit is None:
            result = processor.process(image, source)
            cache.put(key, result)
    """

    def __init__(self, max_size: int = 64):
        self._max_size = max(1, max_size)
        self._cache: OrderedDict[str, object] = OrderedDict()
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    @staticmethod
    def hash_key(data: bytes) -> str:
        """Compute SHA-256 hex digest of raw image bytes."""
        return hashlib.sha256(data).hexdigest()

    def get(self, key: str):
        """Look up a cached FaceResult. Returns None on miss."""
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._hits += 1
                logger.debug("Cache HIT (%s…)", key[:12])
                return self._cache[key]
            self._misses += 1
            return None

    def put(self, key: str, value) -> None:
        """Store a FaceResult in the cache, evicting LRU if full."""
        with self._lock:
            if key in self._cache:
                self._cache.move_to_end(key)
                self._cache[key] = value
                return
            self._cache[key] = value
            if len(self._cache) > self._max_size:
                evicted_key, _ = self._cache.popitem(last=False)
                logger.debug("Cache evicted %s…", evicted_key[:12])

    def clear(self) -> None:
        """Clear all cached entries."""
        with self._lock:
            self._cache.clear()
            self._hits = 0
            self._misses = 0

    @property
    def stats(self) -> dict:
        """Return cache hit/miss statistics."""
        with self._lock:
            total = self._hits + self._misses
            return {
                "size": len(self._cache),
                "max_size": self._max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": self._hits / total if total > 0 else 0.0,
            }
