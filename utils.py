import hashlib
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.utils.safestring import mark_safe
from strawberry import UNSET
from strawberry_django.filters import apply as filter_apply
from strawberry_django.pagination import apply as pagination_apply
from strawberry_django.ordering import apply as ordering_apply
from dataclasses import asdict
from django.contrib.auth.decorators import login_required

REDIS_TTL = 86400  # Seconds


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


def generate_id_from_unique_non_model_fields(unique_field_list):
    unique_value = ''.join([str(item) for item in unique_field_list])
    return int(hashlib.sha1(unique_value.encode("utf-8")).hexdigest(), 16) % (10 ** 8)


def get_redis_key(keys):
    keys_list = list(map(''.join, keys))
    return '-'.join(
        filter(None, keys_list)
    )


def set_redis_cache_data(*keys, value=None):
    return cache.set(get_redis_key(keys), value, REDIS_TTL)


def get_redis_cache_data(*keys):
    return cache.get(get_redis_key(keys))


def get_values_list_from_dataclass(data_class):
    if data_class:
        return [value for value in asdict(data_class).values() if value != UNSET]
    return []


def clean_filters(filters):
    # Filter out None values
    return {
        k: v
        for k, v in filters.items()
        if v is not None
    }


@login_required
def cache_clear(request):
    cache.clear()
    messages.add_message(request, messages.INFO, mark_safe("Cache Cleared"))
    return HttpResponseRedirect(reverse('admin:index'))


def str_to_bool(value):
    # https://github.com/django/django/blob/c765b62e3258de4dce9935ab7aed430346dfbc10/django/forms/fields.py#L790-L800
    if isinstance(value, str) and value.lower() in ("false", "0"):
        return False
    return bool(value)


async def get_filtered_ordered_paginated_qs(
    qs, filters, order, pagination
):
    if filters:
        qs = filter_apply(filters, qs)
    if order:
        qs = ordering_apply(order, qs)
    if pagination:
        qs = pagination_apply(pagination, qs)
    return await get_async_list_from_queryset(qs)


@login_required
def sync_filter_options(request):

    from apps.visualization.models import DataCountryLevel
    from apps.migrate_csv.models import CachedCountryFilterOptions

    # Remove old filter options
    CachedCountryFilterOptions.objects.all().delete()
    # Get distinct values queryset
    qs = DataCountryLevel.objects.values(
        'iso3', 'emergency', 'indicator_id', 'indicator_description', 'subvariable', 'type',
    ).distinct(
        'iso3', 'emergency', 'indicator_id', 'indicator_description', 'subvariable', 'type',
    )
    CachedCountryFilterOptions.objects.bulk_create([
        CachedCountryFilterOptions(
            iso3=item['iso3'],
            emergency=item['emergency'],
            indicator_id=item['indicator_id'],
            indicator_description=item['indicator_description'],
            subvariable=item['subvariable'],
            type=item['type'],
        ) for item in qs
    ])
    messages.add_message(
        request,
        messages.INFO, mark_safe(f'Synced {qs.count()} distinct filter options')
    )
    return HttpResponseRedirect(reverse('admin:index'))
