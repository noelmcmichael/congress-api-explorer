"""
Caching utilities for Congress API Explorer.
"""

import json
import time
from abc import ABC, abstractmethod
from typing import Any, Optional, Dict, Union
from hashlib import md5

from .config import settings, get_cache_ttl
from .logging import logger


class CacheBackend(ABC):
    """Abstract base class for cache backends."""
    
    @abstractmethod
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass
    
    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in cache with optional TTL."""
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        """Delete value from cache."""
        pass
    
    @abstractmethod
    async def clear(self) -> bool:
        """Clear all cache entries."""
        pass


class MemoryCache(CacheBackend):
    """In-memory cache implementation."""
    
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from memory cache."""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        # Check if expired
        if entry.get("expires_at") and time.time() > entry["expires_at"]:
            del self._cache[key]
            return None
        
        logger.debug(f"Cache hit for key: {key}")
        return entry["value"]
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in memory cache."""
        try:
            entry = {
                "value": value,
                "created_at": time.time(),
                "expires_at": time.time() + ttl if ttl else None
            }
            self._cache[key] = entry
            logger.debug(f"Cache set for key: {key}, TTL: {ttl}")
            return True
        except Exception as e:
            logger.error(f"Failed to set cache for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from memory cache."""
        if key in self._cache:
            del self._cache[key]
            logger.debug(f"Cache deleted for key: {key}")
            return True
        return False
    
    async def clear(self) -> bool:
        """Clear all memory cache entries."""
        self._cache.clear()
        logger.info("Memory cache cleared")
        return True


class RedisCache(CacheBackend):
    """Redis cache implementation."""
    
    def __init__(self):
        self._redis = None
        self._initialized = False
    
    async def _init_redis(self):
        """Initialize Redis connection."""
        if self._initialized:
            return
        
        try:
            import redis.asyncio as redis
            self._redis = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                db=settings.redis_db,
                password=settings.redis_password,
                decode_responses=True
            )
            # Test connection
            await self._redis.ping()
            self._initialized = True
            logger.info("Redis cache initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Redis cache: {e}")
            raise
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        await self._init_redis()
        try:
            value = await self._redis.get(key)
            if value:
                logger.debug(f"Redis cache hit for key: {key}")
                return json.loads(value)
            return None
        except Exception as e:
            logger.error(f"Failed to get from Redis cache for key {key}: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        """Set value in Redis cache."""
        await self._init_redis()
        try:
            serialized_value = json.dumps(value, default=str)
            await self._redis.set(key, serialized_value, ex=ttl)
            logger.debug(f"Redis cache set for key: {key}, TTL: {ttl}")
            return True
        except Exception as e:
            logger.error(f"Failed to set Redis cache for key {key}: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from Redis cache."""
        await self._init_redis()
        try:
            result = await self._redis.delete(key)
            logger.debug(f"Redis cache deleted for key: {key}")
            return result > 0
        except Exception as e:
            logger.error(f"Failed to delete from Redis cache for key {key}: {e}")
            return False
    
    async def clear(self) -> bool:
        """Clear all Redis cache entries."""
        await self._init_redis()
        try:
            await self._redis.flushdb()
            logger.info("Redis cache cleared")
            return True
        except Exception as e:
            logger.error(f"Failed to clear Redis cache: {e}")
            return False


class CacheManager:
    """Cache manager that handles different cache backends."""
    
    def __init__(self):
        self._backend: Optional[CacheBackend] = None
    
    def _get_backend(self) -> CacheBackend:
        """Get or create cache backend."""
        if self._backend is None:
            if settings.cache_type.lower() == "redis":
                self._backend = RedisCache()
            else:
                self._backend = MemoryCache()
        return self._backend
    
    def _make_key(self, *args, **kwargs) -> str:
        """Create cache key from arguments."""
        key_parts = []
        for arg in args:
            key_parts.append(str(arg))
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}={v}")
        
        key_string = "|".join(key_parts)
        return md5(key_string.encode()).hexdigest()
    
    async def get(self, cache_type: str, *args, **kwargs) -> Optional[Any]:
        """Get cached value."""
        key = self._make_key(cache_type, *args, **kwargs)
        backend = self._get_backend()
        return await backend.get(key)
    
    async def set(self, cache_type: str, value: Any, *args, **kwargs) -> bool:
        """Set cached value."""
        key = self._make_key(cache_type, *args, **kwargs)
        ttl = get_cache_ttl(cache_type)
        backend = self._get_backend()
        return await backend.set(key, value, ttl)
    
    async def delete(self, cache_type: str, *args, **kwargs) -> bool:
        """Delete cached value."""
        key = self._make_key(cache_type, *args, **kwargs)
        backend = self._get_backend()
        return await backend.delete(key)
    
    async def clear(self) -> bool:
        """Clear all cached values."""
        backend = self._get_backend()
        return await backend.clear()


# Global cache manager instance
cache_manager = CacheManager()