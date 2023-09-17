from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

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
    permission_classes=[permissions.IsAuthenticated],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("users/", include("apps.users.urls")),
    path("dependents/", include("apps.dependents.urls")),
    path("schemes/", include("apps.schemes.urls")),
    path("prices/", include("apps.prices.urls")),
    path("policies/", include("apps.policies.urls")),
    path("claims/", include("apps.claims.urls")),
    path("sales/", include("apps.sales.urls")),
    path("entities/", include("apps.entities.urls")),
    path("reports/", include("apps.reports.urls")),
    path("payments/", include("apps.payments.urls")),
    path("petinsure/", include("apps.pet_insure.urls")),
    path("core/", include("apps.core.urls")),
    path("", schema_view.with_ui("swagger", cache_timeout=0),
         name="schema-swagger-ui",),
    path("redoc/", schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings)
