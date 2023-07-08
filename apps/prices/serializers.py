from rest_framework import serializers
from apps.prices.models import PricingPlan, PricingPlanCoverMapping, PricingPlanExtendedPremiumMapping

from rest_framework_bulk import (
    BulkSerializerMixin,
)


class PricingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingPlan
        fields = "__all__"

class PricingPlanExtendedPremiumMappingSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = PricingPlanExtendedPremiumMapping
        fields = "__all__"

class PricingPlanBulkUploadSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = PricingPlan
        fields = "__all__"


class PricingPlanCoverMappingSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = PricingPlanCoverMapping
        fields = "__all__"


class DependentPricingSerializer(serializers.Serializer):
    date_of_birth = serializers.DateField()
    dependent_type = serializers.CharField(max_length=255)