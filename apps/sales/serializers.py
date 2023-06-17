from rest_framework import serializers
from apps.sales.models import FailedUploadData, TemporaryDataHolding, TemporaryMemberData

from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)


class BulkTemporaryMemberDataSerializer(serializers.Serializer):
    onboarding_mode = serializers.CharField(max_length=255)
    upload_type = serializers.CharField(max_length=255)
    upload_data = serializers.JSONField()
   
   


class TelesalesBulkTemporaryMemberDataSerializer(serializers.ModelSerializer):
    onboarding_mode = serializers.CharField(max_length=255)
    upload_type = serializers.CharField(max_length=255)
    upload_data = serializers.JSONField()


class NewMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryMemberData
        fields = "__all__"


class BulkTemporaryPaidMemberDataBulkSerializer(serializers.Serializer):
    onboarding_mode = serializers.CharField(max_length=255)
    upload_type = serializers.CharField(max_length=255)
    upload_data = serializers.JSONField()


class BulkPolicyCreateSerializer(serializers.Serializer):
    file = serializers.FileField()
    # policy_number = serializers.CharField(max_length=255)
    scheme_group_id = serializers.IntegerField()
    # pricing_plan = serializers.CharField(max_length=255)


class BulkTemporaryNewMemberUploadSerializer(serializers.Serializer):
    onboarding_mode = serializers.CharField(max_length=255)
    upload_type = serializers.CharField(max_length=255)
    upload_data = serializers.JSONField()


class BulkTemporaryDependentUploadSerializer(serializers.Serializer):
    onboarding_mode = serializers.CharField(max_length=255)
    upload_type = serializers.CharField(max_length=255)
    upload_data = serializers.JSONField()


class BulkTemporaryMemberCancellationUploadSerializer(serializers.Serializer):
    onboarding_mode = serializers.CharField(max_length=255)
    upload_type = serializers.CharField(max_length=255)
    upload_data = serializers.JSONField()


class BulkTemporaryLapseDataUploadSerializer(serializers.ModelSerializer):
    onboarding_mode = serializers.CharField(
        max_length=255, default='background', required=False)
    upload_data = serializers.JSONField()


class TemporaryDataHoldingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryDataHolding
        fields = "__all__"


class MembersOnboardingInitiateSerializer(serializers.Serializer):
    pass


class FailedUploadDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = FailedUploadData
        fields = "__all__"


class PolicyPurchaseSerializer(serializers.Serializer):
    seller_details = serializers.JSONField()
    members = serializers.JSONField()
    dependents = serializers.JSONField()
    extended_dependents = serializers.JSONField()
    beneficiaries = serializers.JSONField()
    

class CreditLifePolicyPurchaseSerializer(serializers.Serializer):
    seller_details = serializers.JSONField()
    members = serializers.JSONField()
    obligations = serializers.JSONField()
    beneficiaries = serializers.JSONField()