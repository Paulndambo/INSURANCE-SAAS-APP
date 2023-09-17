from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.pet_insure.views import BreedViewSet, PetViewSet

router = DefaultRouter()
router.register("pets", PetViewSet, basename="pets")
router.register("pet-breeds", BreedViewSet, basename="pet-breeds"),

urlpatterns = [
    path("", include(router.urls)),
]