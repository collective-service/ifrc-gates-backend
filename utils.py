async def get_async_list_from_queryset(qs):
    return [
        item async for item in qs
    ]
