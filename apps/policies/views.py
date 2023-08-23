from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from apps.policies.models import Policy, PolicyCancellation, PolicyStatusUpdates, CycleStatusUpdates, Cycle
from apps.policies.serializers import (
    PolicySerializer,
    PolicyCancellationSerializer,
    # PolicyStatusUpdatesSerializer,
    CycleSerializer,
    CycleStatusUpdatesSerializer,
    PolicyStatusUpdatesSerializer
)


# Create your views here.
class PolicyModelViewSet(ModelViewSet):
    queryset = Policy.objects.all().order_by("-created")
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



class PolicyStatusUpdateViewSet(ModelViewSet):
    queryset = PolicyStatusUpdates.objects.all()
    serializer_class = PolicyStatusUpdatesSerializer

    def get_queryset(self):
        policy = self.request.query_params.get("policy")

        if policy:
            return self.queryset.filter(policy_id=policy)
        return self.queryset