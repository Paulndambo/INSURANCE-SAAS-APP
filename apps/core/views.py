from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from apps.core.models import Insurer
from apps.core.serializers import InsurerSerializer
# Create your views here.
class InsurerViewSet(ModelViewSet):
    queryset = Insurer.objects.all()
    serializer_class = InsurerSerializer