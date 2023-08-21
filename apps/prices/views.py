from django.shortcuts import render
from django.db.models import Q
from apps.prices.models import (
    PricingPlan, 
    PricingPlanCoverMapping, 
    PricingPlanExtendedPremiumMapping,
    Obligation
)
from rest_framework.permissions import AllowAny
from apps.prices.serializers import (
    PricingPlanSerializer,
    PricingPlanBulkUploadSerializer,
    PricingPlanCoverMappingSerializer, 
    DependentPricingSerializer,
    PricingPlanExtendedPremiumMappingSerializer,
    ObligationSerializer
)

from rest_framework_bulk import (
    ListBulkCreateUpdateDestroyAPIView,
)

from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.constants.shared_methods import calculate_age, date_format_method
from apps.constants.type_checking_methods import check_if_value_is_date
from apps.constants.utils import CustomPagination
from apps.prices.main_members_pricing_methods import get_main_member_premium


# Create your views here.
class ObligationViewSet(ModelViewSet):
    queryset = Obligation.objects.all()
    serializer_class = ObligationSerializer


    def get_queryset(self):
        policy = self.request.query_params.get("policy")
        membership = self.request.query_params.get("membership")

        if policy and membership:
            return self.queryset.filter(policy_id=policy, membership=membership)
        else:
            return []


class PricingPlanViewSet(ModelViewSet):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer
    pagination_class = CustomPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        group = self.request.query_params.get("group")
        if group:
            return self.queryset.filter(group=group)
        else:
            return self.queryset


class PricingPlanAPIView(APIView):
    def get(self, request, *args, **kwargs):
        plan_name = self.request.query_params.get("plan_name")
        if plan_name == "null":
            return Response({})

        if plan_name:
            plan = PricingPlan.objects.filter(name=plan_name).values().first()
            return Response(plan)
        return Response({})


class BulkPricingPlanUploadAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanBulkUploadSerializer


class PricingPlanExtendedPremiumMappingAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = PricingPlanExtendedPremiumMapping.objects.all()
    serializer_class = PricingPlanExtendedPremiumMappingSerializer


class PricingPlanCoverMappingAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = PricingPlanCoverMapping.objects.all()
    serializer_class = PricingPlanCoverMappingSerializer


class MainMemberPricingAPIView(APIView):
    def get(self, request, **kwargs):
        pricing_plan_name = request.query_params.get("pricing_plan")
        cover_amount = int(request.query_params.get("cover_amount"))

        prem = 0
        if pricing_plan_name and cover_amount:
            pricing_plan = PricingPlan.objects.filter(name__in=[pricing_plan_name, pricing_plan_name.title()]).first()
            cover_levels = pricing_plan.policy_holder_cover_levels
            prem = get_main_member_premium(cover_levels, cover_amount)
            
        return Response(prem)


class DependentPricingAPIView(APIView):
    
    def get(self, request, **kwargs):
        pricing_plan = request.query_params.get("pricing_plan")
        dependent_type = request.query_params.get("dependent_type")
        date_of_birth = request.query_params.get("date_of_birth")

        cover_level = 0

        if pricing_plan == "null" or date_of_birth == "null" or dependent_type == "null":
            cover_level = 0

        if pricing_plan  and dependent_type and date_of_birth:
            dob = date_of_birth if check_if_value_is_date(date_of_birth) == True else date_format_method(date_of_birth)
            age = calculate_age(dob)

            covers = PricingPlanCoverMapping.objects.filter(pricing_plan__name=pricing_plan, relationship__relative_name__in=[
                                                            dependent_type, dependent_type.capitalize(), dependent_type.lower()])

            for cover in covers:
                if age in range(cover.min_age, cover.max_age + 1):
                    cover_level = cover.cover_level
          
        return Response(cover_level)
    

class ExtendedDependentPricingAPIView(APIView):

    def get(self, request, **kwargs):
        pricing_plan = request.query_params.get("pricing_plan")
        date_of_birth = request.query_params.get("date_of_birth")
        cover_level = request.query_params.get("cover_level")

        add_on_premium = 0
        if pricing_plan == "null" or date_of_birth == "null" or cover_level == "null":
            add_on_premium = 0

        if pricing_plan  and date_of_birth and cover_level:
            dob = date_of_birth if check_if_value_is_date(date_of_birth) == True else date_format_method(date_of_birth)
            age = calculate_age(dob)

            premiums_list = PricingPlanExtendedPremiumMapping.objects.filter(pricing_plan=pricing_plan, cover_level=cover_level)
            for cover in premiums_list:
                if age in range(cover.min_age, cover.max_age + 1):
                    add_on_premium = cover.extended_premium

        return Response(add_on_premium)
    

class ExtendedCoverLevelsAPIView(APIView):

    def get(self, request, **kwargs):
        pricing_plan = request.query_params.get("pricing_plan")
        
        cover_levels = []
        if pricing_plan == "null":
            cover_levels = []

        if pricing_plan:
            levels = PricingPlanExtendedPremiumMapping.objects.filter(pricing_plan=pricing_plan)
            cover_levels = set([x.cover_level for x in levels])

        return Response(cover_levels)