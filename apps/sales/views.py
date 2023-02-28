from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework_bulk import (
    ListBulkCreateUpdateDestroyAPIView,
)

from rest_framework import generics
from rest_framework.response import Response
from apps.sales.models import (
    TemporaryDependentImport,
    TemporaryDataHolding,
    TemporaryCancelledMemberData,
    TemporaryMemberData,
    TemporaryPaidMemberData,
    PricingPlanSchemeMapping,
)

from apps.sales.serializers import (
    TemporaryCancelledMemberDataUploadSerializer,
    TemporaryDataHoldingUploadSerializer,
    TemporaryDepedentDataUploadSerializer,
    TemporaryNewMemberUploadSerializer,
    TemporaryPaidMemberDataUploadSerializer,
    PricingPlanSchemeMappingSerializer
)


# Create your views here.
class TemporaryNewMemberDataAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = TemporaryMemberData.objects.all()
    serializer_class = TemporaryNewMemberUploadSerializer
    permission_classes = [AllowAny]


class PricingPlanSchemeMappingAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = PricingPlanSchemeMapping.objects.all()
    serializer_class = PricingPlanSchemeMappingSerializer
    permission_classes = [AllowAny]


class TemporaryCancelledMemberDataAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = TemporaryCancelledMemberData.objects.all()
    serializer_class = TemporaryCancelledMemberDataUploadSerializer
    permission_classes = [AllowAny]


class TemporaryPaidMemberDataAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = TemporaryPaidMemberData.objects.all()
    serializer_class = TemporaryPaidMemberDataUploadSerializer
    permission_classes = [AllowAny]


class TemporaryDataHoldingAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = TemporaryDataHolding.objects.all()
    serializer_class = TemporaryDataHoldingUploadSerializer
    permission_classes = [AllowAny]


class TemporaryDependentDataAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = TemporaryDependentImport.objects.all()
    serializer_class = TemporaryDepedentDataUploadSerializer
    permission_classes = [AllowAny]


class GenerateGWPReportAPIView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Hello World"})
