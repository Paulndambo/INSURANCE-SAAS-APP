from rest_framework import serializers
from apps.dependents.models import Beneficiary, Dependent, FamilyMemberPricing
from apps.policies.models import Policy
from apps.schemes.models import SchemeGroup


class BeneficiarySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Beneficiary
        fields = "__all__"


    def create(self, validated_data):
        membership = self.context.get("membership_pk")
        scheme_group = self.context.get("scheme_group_pk")

        if membership and scheme_group:
            schemegroup = SchemeGroup.objects.get(id=scheme_group)
            return Beneficiary.objects.create(
                policy=schemegroup.policy,
                membership_id=membership,
                schemegroup=schemegroup,
                **validated_data
            )
        return Beneficiary.objects.create(
            **validated_data
        )


class DependentSerializer(serializers.ModelSerializer):
    relative = serializers.SerializerMethodField()
    class Meta:
        model = Dependent
        fields = "__all__"

    
    def get_relative(self, obj):
        return obj.relative.relative_name


    def create(self, validated_data):
        membership = self.context.get("membership_pk")
        scheme_group = self.context.get("scheme_group_pk")

        if membership and scheme_group:
            schemegroup = SchemeGroup.objects.get(id=scheme_group)
            return Dependent.objects.create(
                policy=schemegroup.policy,
                membership_id=membership,
                schemegroup=schemegroup,
                **validated_data
            )
        return Dependent.objects.create(
            **validated_data
        )


class FamilyMemberPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FamilyMemberPricing
        fields = "__all__"