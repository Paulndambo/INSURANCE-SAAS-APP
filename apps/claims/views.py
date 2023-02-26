from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from apps.claims.models import (
    Claim,
    ClaimDocument,
    ClaimStatusUpdates,
    ClaimAdditionalInfo,
)
from apps.claims.serializers import (
    ClaimDocumentSerializer,
    ClaimSerializer,
    ClaimStatusUpdatesSerializer,
    ClaimAdditionalInfoSerializer,
)


# Create your views here.
class ClaimModelViewSet(ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer


class ClaimDocumentModelViewSet(ModelViewSet):
    queryset = ClaimDocument.objects.all()
    serializer_class = ClaimDocumentSerializer


class ClaimStatusUpdatesModelViewSet(ModelViewSet):
    queryset = ClaimStatusUpdates.objects.all()
    serializer_class = ClaimStatusUpdatesSerializer


class ClaimAdditionalInfoModelViewSet(ModelViewSet):
    queryset = ClaimAdditionalInfo.objects.all()
    serializer_class = ClaimAdditionalInfoSerializer
