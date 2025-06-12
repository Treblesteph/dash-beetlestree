# cache.py
import os
import redis
import pickle
import urllib.parse

# Use REDIS_URL if defined (e.g. in Railway), otherwise default to local Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
parsed = urllib.parse.urlparse(REDIS_URL)

# Create Redis client
r = redis.Redis(
    host=parsed.hostname,
    port=parsed.port,
    password=parsed.password,
    ssl=parsed.scheme == "rediss"
)

def cache_get(key):
    """Retrieve pickled Python object from Redis."""
    try:
        val = r.get(key)
        return pickle.loads(val) if val else None
    except Exception as e:
        print(f"[Redis GET] Error for key '{key}': {e}")
        return None

def cache_set(key, value, ttl=3600):
    """Store pickled Python object in Redis with optional TTL (in seconds)."""
    try:
        r.set(key, pickle.dumps(value), ex=ttl)
    except Exception as e:
        print(f"[Redis SET] Error for key '{key}': {e}")
