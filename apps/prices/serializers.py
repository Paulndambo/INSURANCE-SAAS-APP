from rest_framework import serializers
from apps.prices.models import PricingPlan

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
