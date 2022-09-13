async def get_async_list_from_queryset(qs):
    return [
        item async for item in qs
    ]


def generate_id_from_unique_fields(obj):
    unique_value = ''.join(
        [
            str(
                getattr(obj, item)
            ) for item in obj._meta.model._meta.unique_together[0]
        ]
    )
    return abs(hash(unique_value)) % (10 ** 8)
