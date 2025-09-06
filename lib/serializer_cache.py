"""
Serializer Cache Manager
Serializer instance-ları cache etmək üçün utility class
"""
from django.core.cache import cache
import hashlib
import json
import pickle

class SerializerCacheManager:
    """Serializer instance-ları cache etmək üçün manager"""
    
    @staticmethod
    def get_cache_key(serializer_class, data, context=None):
        """Cache key yaradır"""
        try:
            # Data-nı JSON-a çevir
            if hasattr(data, '__dict__'):
                data_str = json.dumps(data.__dict__, sort_keys=True, default=str)
            else:
                data_str = json.dumps(data, sort_keys=True, default=str)
            
            # Context-i JSON-a çevir
            context_str = json.dumps(context or {}, sort_keys=True, default=str)
            
            # Content yarad
            content = f"{serializer_class.__name__}:{data_str}:{context_str}"
            
            # MD5 hash yarad
            return hashlib.md5(content.encode()).hexdigest()
        except Exception:
            # Fallback - simple key
            return f"serializer_{serializer_class.__name__}_{hash(str(data))}"
    
    @staticmethod
    def get_cached_serializer(serializer_class, data, context=None):
        """Cache-dən serializer alır"""
        try:
            cache_key = SerializerCacheManager.get_cache_key(serializer_class, data, context)
            cached_data = cache.get(cache_key)
            
            if cached_data:
                # Pickle-dan deserialize et
                return pickle.loads(cached_data)
            
            return None
        except Exception:
            return None
    
    @staticmethod
    def cache_serializer(serializer_class, data, context=None, timeout=300):
        """Serializer-i cache-ə yazır"""
        try:
            cache_key = SerializerCacheManager.get_cache_key(serializer_class, data, context)
            
            # Serializer yarad
            serializer = serializer_class(data, context=context)
            
            # Pickle ilə serialize et
            serialized_data = pickle.dumps(serializer)
            
            # Cache-ə yaz
            cache.set(cache_key, serialized_data, timeout)
            
            return serializer
        except Exception:
            # Fallback - serializer yarad cache olmadan
            return serializer_class(data, context=context)
    
    @staticmethod
    def invalidate_cache(serializer_class, data, context=None):
        """Cache-dən serializer-i silir"""
        try:
            cache_key = SerializerCacheManager.get_cache_key(serializer_class, data, context)
            cache.delete(cache_key)
            return True
        except Exception:
            return False 