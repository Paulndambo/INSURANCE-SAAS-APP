from django.shortcuts import render
from apps.prices.models import PricingPlan
from apps.prices.serializers import PricingPlanSerializer

from rest_framework.viewsets import ModelViewSet
# Create your views here.
class PricingPlanViewSet(ModelViewSet):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer