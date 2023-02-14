from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status

from apps.dependents.models import Beneficiary, Dependent
from apps.dependents.serializers import BeneficiarySerializer, DependentSerializer

# Create your views here.
class DependentModelViewSet(ModelViewSet):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer


class BeneficiaryModelViewSet(ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer