from django.contrib import admin
from django.urls import path, include


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Smart Insure API",
        default_version="v1",
        description="This is the Insure API Service",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="paulkadabo@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("dependents/", include("apps.dependents.urls")),
    path("schemes/", include("apps.schemes.urls")),
    path("prices/", include("apps.prices.urls")),
    path("policies/", include("apps.policies.urls")),
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]
