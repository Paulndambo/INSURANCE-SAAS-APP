from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.entities.serializers import BrokerSerializer, SalesAgentSerializer
from apps.entities.models import Broker, SalesAgent
# Create your views here.
class BrokerViewSet(ModelViewSet):
    queryset = Broker.objects.all()
    serializer_class = BrokerSerializer


class SalesAgentViewSet(ModelViewSet):
    queryset = SalesAgent.objects.all()
    serializer_class = SalesAgentSerializer