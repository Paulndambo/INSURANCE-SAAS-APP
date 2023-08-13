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
        policy_id = self.request.query_params.get("policy_id")
        print("*************Policy ID**********")
        print(policy_id)
        print("*************Policy ID**********")
        if scheme_pk:
            return self.queryset.filter(scheme_id=self.kwargs["scheme_pk"])
        if policy_id:
            return self.queryset.filter(policy__id=int(policy_id))
        else:
            return self.queryset

    def get_serializer_context(self):
        return {"request": self.request}