
import time
from functools import wraps

class Cache:
    def __init__(self):
        self._cache = {}

    def set(self, key, value, expiration=300):  # Default expiration of 5 minutes
        self._cache[key] = (value, time.time() + expiration)

    def get(self, key):
        if key in self._cache:
            value, expiration = self._cache[key]
            if time.time() < expiration:
                return value
            else:
                del self._cache[key]
        return None

    def clear(self):
        self._cache.clear()

cache = Cache()

def cached(expiration=300):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result
            result = await func(*args, **kwargs)
            cache.set(key, result, expiration)
            return result
        return wrapper
    return decorator
