from rest_framework import serializers
from apps.prices.models import (
    PricingPlan, 
    PricingPlanCoverMapping, 
    PricingPlanExtendedPremiumMapping,
    Obligation
)

from rest_framework_bulk import (
    BulkSerializerMixin,
)

class ObligationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obligation
        fields = "__all__"
        

class PricingPlanSerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = PricingPlan
        fields = "__all__"

    def get_category_name(self, obj):
        return obj.category.name

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