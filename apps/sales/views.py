from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework_bulk import (
    ListBulkCreateUpdateDestroyAPIView,
)

from apps.sales.models import (
    TemporaryDependentImport,
    TemporaryDataHolding,
    TemporaryCancelledMemberData,
    TemporaryMemberData,
    TemporaryPaidMemberData,
)

from apps.sales.serializers import (
    TemporaryCancelledMemberDataUploadSerializer,
    TemporaryDataHoldingUploadSerializer,
    TemporaryDepedentDataUploadSerializer,
    TemporaryNewMemberUploadSerializer,
    TemporaryPaidMemberDataUploadSerializer,
)


# Create your views here.
class TemporaryNewMemberDataAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = TemporaryMemberData.objects.all()
    serializer_class = TemporaryNewMemberUploadSerializer
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
