"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from config.graphql import CustomAsyncGraphQLView
from config.schema import schema
from rest_framework import routers
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

from apps.visualization import views
from utils import cache_clear, sync_filter_options

router = routers.DefaultRouter()

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Collective Service API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", CustomAsyncGraphQLView.as_view(schema=schema, graphiql=False)),
    path('tinymce/', include('tinymce.urls')),

    # rest api urls
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    path('api/v1/sources/', views.SourceListAggViews.as_view()),
    path('api/v1/context_indicators/', views.ContextIndicatorsViews.as_view()),
    path('api/v1/export-raw-data/', views.ExportRawDataView.as_view()),
    path('api/v1/export-summary/', views.ExportSummaryView.as_view()),
    path('api/v1/export-country-contextual-data/', views.ExportCountryDataCountryLevelPublicContextView.as_view()),
    path('clear-cache/', cache_clear, name='clear_cache'),
    path('sync-filter-options/', sync_filter_options, name='sync_filter_options'),
    path('health-checkup/', views.HealthCheckupView.as_view(), name="health_checkup")
]

admin.site.site_header = "Collective Service Administration"
admin.site.index_title = "Collective Service Admin Portal"
admin.site.site_title = " "

# Enable debug tool bar and graphiql in local only
if settings.DEBUG:
    urlpatterns = urlpatterns + [
        path("graphiql/", CustomAsyncGraphQLView.as_view(schema=schema)),
    ]

if 'debug_toolbar' in settings.INSTALLED_APPS:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]

# Static and media file urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
