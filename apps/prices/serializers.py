from rest_framework import serializers
from apps.prices.models import PricingPlan, PricingPlanCoverMapping

from rest_framework_bulk import (
    BulkSerializerMixin,
)


class PricingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = "__all__"


class PricingPlanBulkUploadSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = PricingPlan
        fields = "__all__"


class PricingPlanCoverMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlanCoverMapping
        fields = "__all__"


class DependentPricingSerializer(serializers.Serializer):
    date_of_birth = serializers.DateField()
    dependent_type = serializers.CharField(max_length=255)