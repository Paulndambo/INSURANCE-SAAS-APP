from django.shortcuts import render
from apps.prices.models import PricingPlan, PricingPlanCoverMapping
from apps.prices.serializers import (
    PricingPlanSerializer,
    PricingPlanBulkUploadSerializer,
    PricingPlanCoverMappingSerializer, 
    DependentPricingSerializer
)

from rest_framework_bulk import (
    ListBulkCreateUpdateDestroyAPIView,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.response import Response


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


class DependentPricingAPIView(generics.CreateAPIView):
    serializer_class = DependentPricingSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)