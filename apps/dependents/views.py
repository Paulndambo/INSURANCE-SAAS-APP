from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status

from apps.dependents.models import Beneficiary, Dependent
from apps.dependents.serializers import BeneficiarySerializer, DependentSerializer
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class DependentModelViewSet(ModelViewSet):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer

    def get_serializer_context(self):
        return self.kwargs


    def get_queryset(self):
        scheme_group = self.kwargs.get("scheme_group_pk")
        membership = self.kwargs.get("membership_pk")

        if scheme_group and membership:
            membership_id = int(membership)
            scheme_group_id = int(scheme_group)
            queryset = self.queryset.filter(schemegroup_id=scheme_group_id, membership_id=membership_id)
            return queryset
        return self.queryset



class BeneficiaryModelViewSet(ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return self.kwargs

    def get_queryset(self):
        scheme_group = self.kwargs.get("scheme_group_pk")
        membership = self.kwargs.get("membership_pk")

        # TODO: use authentication to separate customer dashboard & admin dashboard

        user = self.request.user
        print(user, user.role)

        if scheme_group and membership:
            membership_id = int(membership)
            scheme_group_id = int(scheme_group)
            #print(type(scheme_group_id))
            queryset = self.queryset.filter(schemegroup_id=scheme_group_id, membership_id=membership_id)
            return queryset
        return self.queryset
        
