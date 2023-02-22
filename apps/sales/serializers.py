from rest_framework import serializers
from rest_framework_bulk import (
    BulkSerializerMixin,
)

from apps.sales.models import (
    TemporaryCancelledMemberData,
    TemporaryDependentImport,
    TemporaryMemberData,
    TemporaryDataHolding,
    TemporaryPaidMemberData,
)


class TemporaryNewMemberUploadSerializer(
    BulkSerializerMixin, serializers.ModelSerializer
):
    class Meta(object):
        model = TemporaryMemberData
        # only necessary in DRF3
        fields = "__all__"


class TemporaryCancelledMemberDataUploadSerializer(
    BulkSerializerMixin, serializers.ModelSerializer
):
    class Meta(object):
        model = TemporaryCancelledMemberData
        fields = "__all__"


class TemporaryDataHoldingUploadSerializer(
    BulkSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = TemporaryDataHolding
        fields = "__all__"


class TemporaryPaidMemberDataUploadSerializer(
    BulkSerializerMixin, serializers.ModelSerializer
):
    class Meta:
        model = TemporaryPaidMemberData
        fields = "__all__"


class TemporaryDepedentDataUploadSerializer(
    BulkSerializerMixin, serializers.ModelSerializer
):
    class Meta(object):
        model = TemporaryDependentImport
        fields = "__all__"
