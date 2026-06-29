import json
from typing import Any, Optional
from core.config import get_settings
from core.logger import logger
from core.exceptions import CacheError

settings = get_settings()

class CacheManager():

    def __init__(self):
        self._client = None

    def _get_client(self):
        if self._client is None:
            import redis
            self._client = redis.Redis(
                host = settings.redis_host,
                port = settings.redis_port,
                password = settings.redis_password or None,
                decode_responses= True,
            )
        return self._client

    def ping(self)-> bool:
        try:
            return self._get_client().ping()
        except Exception:
            return False
        
    def get(self, key:str) -> Optional[Any]:
        try:
            client = self._get_client()
            value= client.get(key)
            if value is None:
                logger.debug(f"Cache MISS -> {key}")
                return None
            logger.debug(f"Cache HIT -> {key}")
            return json.loads(value)
        except Exception as e:
            raise CacheError(
                message= f"Failed to GET key '{key}:{str(e)}",
                operation ="get"
            )
    
    def set(self,key :str,value:Any, ttl:int) -> bool:
        try:
            client = self._get_client()
            serialized = json.dumps(value, default=str)
            client.setex(key, ttl, serialized)
            logger.debug(f"Cache SET -> {key} | TTL = {ttl}s")
            return True
        except Exception as e:
            raise CacheError(
                message= f"Failed to SET key '{key}': {str(e)}",
                operation ="set",
            )
    
    def delete(self, key: str) -> bool:
        try:
            self._get_client().delete(key)
            logger.debug(f"Cache DEL  → {key}")
            return True
        except Exception as e:
            raise CacheError(
                message=f"Failed to DELETE key '{key}': {str(e)}",
                operation="delete",
            )

    def exists(self, key: str) -> bool:
        try:
            return bool(self._get_client().exists(key))
        except Exception:
            return False
    @staticmethod
    def build_key(*parts: str) -> str:
        return ":".join(str(p).upper() for p in parts)
    
Cache= CacheManager()