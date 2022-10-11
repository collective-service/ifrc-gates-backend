import hashlib
from django.core.cache import cache

REDIS_TTL = 86400 # Seconds


async def get_async_list_from_queryset(qs):
    return [
        item async for item in qs
    ]


def generate_id_from_unique_field(unique_value):
    return int(hashlib.sha1(unique_value.encode("utf-8")).hexdigest(), 16) % (10 ** 8)


def generate_id_from_unique_fields(obj):
    unique_value = ''.join(
        [
            str(
                getattr(obj, item)
            ) for item in obj._meta.model._meta.unique_together[0]
        ]
    )
    return int(hashlib.sha1(unique_value.encode("utf-8")).hexdigest(), 16) % (10 ** 8)


def set_redis_cache_data(*keys, value=None):
    redis_key = '-'.join(filter(None, list(keys)))
    return cache.set(redis_key, value, REDIS_TTL)


def get_redis_cache_data(*keys):
    redis_key = '-'.join(filter(None, list(keys)))
    return cache.get(redis_key)
