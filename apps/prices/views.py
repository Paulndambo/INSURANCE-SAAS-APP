from django.shortcuts import render
from apps.prices.models import PricingPlan, PricingPlanCoverMapping
from apps.prices.serializers import (
    PricingPlanSerializer,
    PricingPlanBulkUploadSerializer,
    PricingPlanCoverMappingSerializer, 
)

from rest_framework_bulk import (
    ListBulkCreateUpdateDestroyAPIView,
)

from rest_framework.viewsets import ModelViewSet


# Create your views here.
class PricingPlanViewSet(ModelViewSet):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer


class BulkPricingPlanUploadAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanBulkUploadSerializer


class PricingPlanCoverMappingViewSet(ModelViewSet):
    queryset = PricingPlanCoverMapping.objects.all()
    serializer_class = PricingPlanCoverMappingSerializer