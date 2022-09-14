from rest_framework import (
    viewsets,
)

from .models import DataCountryLevelMostRecent
from .serializers import DataCountryLevelMostRecentSerializer
from .rest_filters import DataCountryLevelMostRecentFilter


class DataCountryLevelMostRecentViewset(viewsets.ReadOnlyModelViewSet):
    queryset = DataCountryLevelMostRecent.objects.all()
    serializer_class = DataCountryLevelMostRecentSerializer
    filterset_class = DataCountryLevelMostRecentFilter
