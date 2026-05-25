import threading
import time
from collections import OrderedDict
from typing import Any, Optional

class TTLCache:
    def __init__(self, max_size=256, ttl=60):
        self.cache = OrderedDict()
        self.ttl = ttl
        self.max_size = max_size
        self.lock = threading.Lock()
        self._start_cleanup_thread()

    def _start_cleanup_thread(self):
        def cleanup():
            while True:
                time.sleep(self.ttl)
                self.cleanup()
        thread = threading.Thread(target=cleanup, daemon=True)
        thread.start()

    def set(self, key: Any, value: Any, ttl: Optional[int] = None):
        with self.lock:
            expire = time.time() + (ttl if ttl else self.ttl)
            self.cache[key] = (value, expire)
            self.cache.move_to_end(key)
            if len(self.cache) > self.max_size:
                self.cache.popitem(last=False)

    def get(self, key: Any, default=None):
        with self.lock:
            item = self.cache.get(key)
            if not item:
                return default
            value, expire = item
            if expire < time.time():
                del self.cache[key]
                return default
            return value

    def has(self, key: Any) -> bool:
        with self.lock:
            item = self.cache.get(key)
            if not item or item[1] < time.time():
                return False
            return True

    def delete(self, key: Any):
        with self.lock:
            if key in self.cache:
                del self.cache[key]

    def clear(self):
        with self.lock:
            self.cache.clear()

    def cleanup(self):
        with self.lock:
            now = time.time()
            remove = [k for k, v in self.cache.items() if v[1] < now]
            for k in remove:
                del self.cache[k]

    def __len__(self):
        with self.lock:
            return sum(1 for _, expire in self.cache.values() if expire >= time.time())
