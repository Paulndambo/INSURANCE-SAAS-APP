from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework import status, generics
from rest_framework.response import Response

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
    LodgeClaimSerializer,
    HelloSerializer
)


# Create your views here.
class LodgeClaimAPIView(generics.CreateAPIView):
    serializer_class = LodgeClaimSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class HelloAPIView(generics.ListCreateAPIView):
    serializer_class = HelloSerializer

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ClaimModelViewSet(ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    def get_queryset(self):
        policy = self.request.query_params.get("policy")

        if policy:
            return self.queryset.filter(policy_id=policy)
        return self.queryset


class ClaimDocumentModelViewSet(ModelViewSet):
    queryset = ClaimDocument.objects.all()
    serializer_class = ClaimDocumentSerializer


class ClaimStatusUpdatesModelViewSet(ModelViewSet):
    queryset = ClaimStatusUpdates.objects.all()
    serializer_class = ClaimStatusUpdatesSerializer


class ClaimAdditionalInfoModelViewSet(ModelViewSet):
    queryset = ClaimAdditionalInfo.objects.all()
    serializer_class = ClaimAdditionalInfoSerializer
