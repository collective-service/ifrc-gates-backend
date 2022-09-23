from strawberry.django.views import AsyncGraphQLView
from starlette.requests import Request
from starlette.responses import Response
from typing import Any, Optional
from strawberry.dataloader import DataLoader

from apps.visualization.dataloaders import (
    load_country_name,
    load_indicator_value_regional,
)


class CustomAsyncGraphQLView(AsyncGraphQLView):

    async def get_context(self, request: Request, response: Optional[Response]) -> Any:
        return {
            'request': request,
            'country_name_loader': DataLoader(load_fn=load_country_name),
            'indicator_value_regional_loader': DataLoader(load_fn=load_indicator_value_regional)
        }
