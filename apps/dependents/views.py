from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.response import Response

from apps.dependents.models import Beneficiary, Dependent, FamilyMemberPricing
from apps.users.models import PolicyHolderRelative
from apps.dependents.serializers import BeneficiarySerializer, DependentSerializer, FamilyMemberPricingSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny



# Create your views here.
class DependentModelViewSet(ModelViewSet):
    queryset = Dependent.objects.all().order_by("-created")
    serializer_class = DependentSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return { "request": self.request }

    def create(self, request, *args, **kwargs):
        data = request.data
        print(data)
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        
        policy = self.request.query_params.get("policy")
        scheme_group = self.request.query_params.get("scheme_group")
        membership = self.request.query_params.get("membership")

        dependent_type = self.request.query_params.get("dependent_type")

        #user = self.request.user
        print(f"Dependent Type: {dependent_type}")

        if dependent_type:
            if dependent_type in ["extended", "Extended"]:
                dependents = self.queryset.filter(dependent_type=dependent_type.lower())
            elif dependent_type in ["dependent", "Dependent"]:
                dependents = self.queryset.filter(dependent_type__in=["Dependent", "dependent"])

            if policy and scheme_group and membership:
                return dependents.filter(policy=policy, schemegroup=scheme_group, membership=membership)

        return self.queryset
            


class BeneficiaryModelViewSet(ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    permission_classes = [AllowAny]

    #def get_serializer_context(self):
    #    return { "request": self.request }

    def get_queryset(self):
        policy = self.request.query_params.get("policy")
        scheme_group = self.request.query_params.get("scheme_group")
        membership = self.request.query_params.get("membership")

    
        if policy and scheme_group and membership:
            return self.queryset.filter(policy=policy, schemegroup=scheme_group, membership=membership)
        return self.queryset
        

class FamilyMemberPricingViewSet(ModelViewSet):
    queryset = FamilyMemberPricing.objects.all()
    serializer_class = FamilyMemberPricingSerializer
    permission_classes = [AllowAny,]