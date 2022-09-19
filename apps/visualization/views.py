from django.db.models import Max, F
from rest_framework.exceptions import ValidationError
from .models import DataCountryLevelMostRecent
from .serializers import DataCountryLevelMostRecentSerializer
from .rest_filters import DataCountryLevelMostRecentFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import ListAPIView


class ContextIndicatorsViews(ListAPIView):
    '''
    Returns most recent inidcator values for a country level.
    It accepts String query parameters such as emergency, region, iso3, type, thematic,
    topic as filter.
    It also accepts query parameters such as limit and offset to request number of objects
    in a page.
    Comma separated string query parameters can be given for topic to filter according
    to multiple topic.
    '''
    default_limit = 10
    serializer_class = DataCountryLevelMostRecentSerializer
    filterset_class = DataCountryLevelMostRecentFilter
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        if self.request.query_params.get('limit'):
            limit = int(self.request.query_params.get('limit'))
            if limit >= 100:
                raise ValidationError({"error": "Limit must be less or equal to 100"})

        result = DataCountryLevelMostRecent.objects.filter(
            category='Global',
        ).order_by(
            '-indicator_month'
        ).values(
            'subvariable'
        ).annotate(
            indicator_name=F('indicator_name'),
            indicator_month=Max('indicator_month'),
            category=F('category'),
            emergency=F('emergency'),
            indicator_value=F('indicator_value'),
            iso3=F('iso3'),
            type=F('type'),
            thematic=F('thematic'),
            topic=F('topic')
        )

        return result

