from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from apps.policies.models import Policy, PolicyCancellation, CycleStatusUpdates, Cycle
from apps.policies.serializers import (
    PolicySerializer,
    PolicyCancellationSerializer,
    # PolicyStatusUpdatesSerializer,
    CycleSerializer,
    CycleStatusUpdatesSerializer
)


# Create your views here.
class PolicyModelViewSet(ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

    def get_serializer_context(self):
        return { "request": self.request }


class PolicyCancellationViewSet(ModelViewSet):
    queryset = PolicyCancellation.objects.all()
    serializer_class = PolicyCancellationSerializer


# class PolicyStatusUpdatesViewSet(ModelViewSet):
#    queryset = PolicyStatusUpdates.objects.all()
#    serializer_class = PolicyStatusUpdatesSerializer

class CycleModelViewSet(ModelViewSet):
    queryset = Cycle.objects.all()
    serializer_class = CycleSerializer


class CycleStatusModelViewSet(ModelViewSet):
    queryset = CycleStatusUpdates.objects.all()
    serializer_class = CycleStatusUpdatesSerializer