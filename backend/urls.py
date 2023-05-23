from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.authtoken.views import obtain_auth_token


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
    path("", include("apps.core.urls")),
    path("users/", include("apps.users.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings)
