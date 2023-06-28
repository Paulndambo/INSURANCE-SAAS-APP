from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.response import Response

from apps.schemes.models import Scheme, SchemeGroup
from apps.schemes.serializers import SchemeSerializer, SchemeGroupSerializer


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
        scheme_pk = self.kwargs.get("scheme_pk")
        if scheme_pk:
            return self.queryset.filter(scheme_id=self.kwargs["scheme_pk"])
        else:
            return self.queryset

    def get_serializer_context(self):
        return {"request": self.request}