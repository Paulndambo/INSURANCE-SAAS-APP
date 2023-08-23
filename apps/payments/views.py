from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

from apps.payments.models import PolicyPremium
from apps.payments.serializers import PolicyPremiumSerializer

# Create your views here.
class PolicyPremiumViewSet(ModelViewSet):
    queryset = PolicyPremium.objects.all()
    serializer_class = PolicyPremiumSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        policy = self.request.query_params.get("policy")

        if policy:
            return self.queryset.filter(policy_id=policy)
        return self.queryset