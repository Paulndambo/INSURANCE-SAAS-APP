from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from apps.policies.models import Policy, PolicyCancellation, PolicyStatusUpdate
from apps.policies.serializers import PolicySerializer, PolicyCancellationSerializer, PolicyStatusUpdateSerializer

# Create your views here.
class PolicyModelViewSet(ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer


class PolicyCancellationViewSet(ModelViewSet):
    queryset = PolicyCancellation.objects.all()
    serializer_class = PolicyCancellationSerializer


class PolicyStatusUpdateViewSet(ModelViewSet):
    queryset = PolicyStatusUpdate.objects.all()
    serializer_class = PolicyStatusUpdateSerializer