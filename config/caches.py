from django.core.cache import caches


local_cache = caches['local-memory']
redis_cache = caches['default']


class CacheKey:
    class AdminNarrativeChoices():
        _base = 'admin_narrative_choices'
        ISO3 = f'{_base}_iso3'
        THEMATIC = f'{_base}_thematic'
        TOPIC = f'{_base}_topic'
        INDICATOR_ID = f'{_base}_indicator_id'
        TTL = 60 * 60 * 10


def redis_cache_func(cache_key, ttl=None):
    def _dec(func):
        def _caller(*args, **kwargs):
            def _func_call():
                return func(*args, **kwargs)
            return redis_cache.get_or_set(cache_key, _func_call, ttl)
        _caller.__name__ = func.__name__
        _caller.__module__ = func.__module__
        return _caller
    return _dec
