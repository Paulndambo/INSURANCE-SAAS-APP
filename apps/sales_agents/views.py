from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.policies.models import Policy
from apps.sales_agents.serializers import SalesAgentPolicySerializer


# Create your views here.
class SalesAgentPolicyViewSet(ModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = SalesAgentPolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if not user.role == "sales_agent":
            return []

        return self.queryset.filter(sold_by__user=user)