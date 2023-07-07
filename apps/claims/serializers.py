from rest_framework import serializers
from apps.claims.models import (
    Claim,
    ClaimDocument,
    ClaimStatusUpdates,
    ClaimAdditionalInfo,
)
#from apps.claims.serializers import ClaimDocumentSerializer, ClaimAdditionalInfoSerializer, ClaimStatusUpdatesSerializer


class ClaimSerializer(serializers.ModelSerializer):
    claim_documents = serializers.SerializerMethodField()
    claimants = serializers.SerializerMethodField()
    claim_additional_info = serializers.SerializerMethodField()
    claim_status_updates = serializers.SerializerMethodField()
    class Meta:
        model = Claim
        fields = "__all__"

    
    def get_claim_documents(self, obj):
        return obj.claimdocuments.values()
    

    def get_claimants(self, obj):
        return obj.claimants.values()
    
    
    def get_claim_additional_info(self, obj):
        return obj.claimadditionalinfo.values()
    
    def get_claim_status_updates(self, obj):
        return obj.claimstatuses.values()


class ClaimDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimDocument
        fields = "__all__"


class ClaimStatusUpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimStatusUpdates
        fields = "__all__"


class ClaimAdditionalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimAdditionalInfo
        fields = "__all__"


class LodgeClaimSerializer(serializers.Serializer):
    policy_details = serializers.JSONField()
    claimant = serializers.JSONField()
    claim_documents = serializers.JSONField()


class HelloSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=255)