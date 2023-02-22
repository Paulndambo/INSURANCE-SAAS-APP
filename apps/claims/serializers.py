from rest_framework import serializers
from apps.claims.models import (
    Claim,
    ClaimDocument,
    ClaimStatusUpdates,
    ClaimAdditionalInfo,
)


class ClaimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Claim
        fields = "__all__"


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
