from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status

from apps.dependents.models import Beneficiary, Dependent, FamilyMemberPricing
from apps.dependents.serializers import BeneficiarySerializer, DependentSerializer, FamilyMemberPricingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class DependentModelViewSet(ModelViewSet):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return { "request": self.request }

    def get_queryset(self):
        scheme_group_id = self.kwargs.get("scheme_group_pk")
        membership_id = self.kwargs.get("membership_pk")
        if scheme_group_id and membership_id:
            return self.queryset.filter(schemegroup_id=scheme_group_id, membership_id=membership_id)
        return self.queryset



class BeneficiaryModelViewSet(ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return { "request": self.request }

    def get_queryset(self):
        scheme_group = self.kwargs.get("scheme_group_pk")
        membership = self.kwargs.get("membership_pk")
        user = self.request.user

        if scheme_group and membership:
            membership_id = int(membership)
            scheme_group_id = int(scheme_group)
            queryset = self.queryset.filter(schemegroup_id=scheme_group_id, membership_id=membership_id)
            return queryset
        return self.queryset
        

class FamilyMemberPricingViewSet(ModelViewSet):
    queryset = FamilyMemberPricing.objects.all()
    serializer_class = FamilyMemberPricingSerializer
    permission_classes = [AllowAny,]