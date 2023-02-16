from rest_framework import serializers
from apps.claims.models import Claim, ClaimDocument, ClaimStatusUpdates


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