from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.schemes.models import Scheme, SchemeGroup
from apps.schemes.serializers import SchemeGroupSerializer, SchemeSerializer


# Create your views here.
class SchemeModelViewSet(ModelViewSet):
    queryset = Scheme.objects.all()
    serializer_class = SchemeSerializer

    def get_serializer_context(self):
        return {"request": self.request}


class SchemeGroupModelViewSet(ModelViewSet):
    queryset = SchemeGroup.objects.all().order_by("-created")
    serializer_class = SchemeGroupSerializer

    def get_queryset(self):
        scheme = self.request.query_params.get("scheme")
        
        if scheme:
            return self.queryset.filter(scheme_id=scheme)
        
        else:
            return self.queryset

    def get_serializer_context(self):
        return {"request": self.request}