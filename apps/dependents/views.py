from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status

from apps.dependents.models import Beneficiary, Dependent, FamilyMemberPricing
from apps.dependents.serializers import BeneficiarySerializer, DependentSerializer, FamilyMemberPricingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

from apps.schemes.models import SchemeGroup
from apps.users.models import Membership



# Create your views here.
class DependentModelViewSet(ModelViewSet):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return { "request": self.request }

    def get_queryset(self):
        scheme_group_id = self.kwargs.get("scheme_group_pk")
        membership_id = self.kwargs.get("membership_pk")
        policy_id = self.kwargs.get("policy_pk")
        user = self.request.user
        
        user_role = user.role
        print(f"Role: {user_role}, Username: {user.username}, Email: {user.email}")
        if policy_id:
            if user_role == "individual":  # individual
                scheme_group = SchemeGroup.objects.get(policy_id=policy_id)
                membership = Membership.objects.filter(user=user, scheme_group=scheme_group, policy_id=policy_id).first()
                if membership:
                    return self.queryset.filter(schemegroup=scheme_group, membership=membership)
                return []
            else:
                return self.queryset.filter(policy_id=policy_id)
        if scheme_group_id and membership_id:
            return self.queryset.filter(schemegroup_id=scheme_group_id, membership_id=membership_id)
        return self.queryset


class BeneficiaryModelViewSet(ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        return { "request": self.request }

    def get_queryset(self):
        scheme_group_id = self.kwargs.get("scheme_group_pk")
        membership_id = self.kwargs.get("membership_pk")
        policy_id = self.kwargs.get("policy_pk")
        user = self.request.user

        user_role = user.role
        print(f"Role: {user_role}, Username: {user.username}, Email: {user.email}")
        if policy_id:
            if user_role == "individual":  # individual
                scheme_group = SchemeGroup.objects.get(policy_id=policy_id)
                membership = Membership.objects.filter(
                    user=user, scheme_group=scheme_group, policy_id=policy_id).first()
                if membership:
                    return self.queryset.filter(schemegroup=scheme_group, membership=membership)
                return []
            else:
                return self.queryset.filter(policy_id=policy_id)
        if scheme_group_id and membership_id:
            return self.queryset.filter(schemegroup_id=scheme_group_id, membership_id=membership_id)
        return self.queryset
        

class FamilyMemberPricingViewSet(ModelViewSet):
    queryset = FamilyMemberPricing.objects.all()
    serializer_class = FamilyMemberPricingSerializer
    permission_classes = [AllowAny,]