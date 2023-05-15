from django.urls import path, include
#from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

## App Views
from apps.schemes.views import SchemeGroupModelViewSet, SchemeModelViewSet


## Other App Views
#from apps.users.views import MembershipViewSet
from apps.dependents.views import DependentModelViewSet, BeneficiaryModelViewSet

router = routers.DefaultRouter()
router.register("schemes", SchemeModelViewSet, basename="schemes")
router.register("scheme-groups", SchemeGroupModelViewSet, basename="scheme-groups")


urlpatterns = [
    path("", include(router.urls)),
  
]
