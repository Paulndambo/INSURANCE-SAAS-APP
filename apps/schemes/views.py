from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet


from apps.schemes.models import Scheme, SchemeGroup
from apps.schemes.serializers import SchemeSerializer, SchemeGroupSerializer
# Create your views here.
class SchemeModelViewSet(ModelViewSet):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer


class SchemeGroupModelViewSet(ModelViewSet):
    queryset = SchemeGroup.objects.all()
    serializer_class = SchemeGroupSerializer