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

router = routers.DefaultRouter()

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="IFRC Gates API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("graphql/", CustomAsyncGraphQLView.as_view(schema=schema, graphiql=False)),

    # rest api urls
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/v1/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
    path('api/v1/context_indicators/', views.ContextIndicatorsViews.as_view()),
]

admin.site.site_header = "IFRC-Gates administration"

# Enable graphiql in local only
if settings.DEBUG:
    urlpatterns.append(path("graphiql/", CustomAsyncGraphQLView.as_view(schema=schema)))

# Static and media file urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
