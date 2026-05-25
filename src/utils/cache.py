import threading
import time
from typing import Any, Optional

class TTLCache:
    def __init__(self, max_size: int = 1000, ttl: float = 60.0, cleanup_interval: float = 10.0):
        self.max_size = max_size
        self.ttl = ttl
        self.cache = {}
        self.expiry = {}
        self.lock = threading.Lock()
        self.cleanup_thread = threading.Thread(target=self._background_cleanup, args=(cleanup_interval,), daemon=True)
        self.cleanup_thread.start()

    def set(self, key: Any, value: Any, ttl: Optional[float] = None):
        with self.lock:
            if len(self.cache) >= self.max_size:
                self._remove_oldest()
            self.cache[key] = value
            self.expiry[key] = time.time() + (ttl if ttl is not None else self.ttl)

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        with self.lock:
            if key in self.cache and self.expiry[key] > time.time():
                return self.cache[key]
            else:
                self.delete(key)
                return default

    def has(self, key: Any) -> bool:
        with self.lock:
            return key in self.cache and self.expiry[key] > time.time()

    def delete(self, key: Any):
        with self.lock:
            self.cache.pop(key, None)
            self.expiry.pop(key, None)

    def clear(self):
        with self.lock:
            self.cache.clear()
            self.expiry.clear()

    def _remove_oldest(self):
        oldest_key = min(self.expiry, key=lambda k: self.expiry[k], default=None)
        if oldest_key is not None:
            self.delete(oldest_key)

    def _background_cleanup(self, interval):
        while True:
            with self.lock:
                now = time.time()
                keys_to_delete = [key for key, exp in self.expiry.items() if exp <= now]
                for key in keys_to_delete:
                    self.delete(key)
            time.sleep(interval)
