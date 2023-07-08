from django.shortcuts import render
from django.db.models import Q
from apps.prices.models import PricingPlan, PricingPlanCoverMapping, PricingPlanExtendedPremiumMapping
from apps.prices.serializers import (
    PricingPlanSerializer,
    PricingPlanBulkUploadSerializer,
    PricingPlanCoverMappingSerializer, 
    DependentPricingSerializer,
    PricingPlanExtendedPremiumMappingSerializer
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


# Create your views here.
class PricingPlanViewSet(ModelViewSet):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanSerializer


class BulkPricingPlanUploadAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = PricingPlan.objects.all()
    serializer_class = PricingPlanBulkUploadSerializer


class PricingPlanExtendedPremiumMappingAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = PricingPlanExtendedPremiumMapping.objects.all()
    serializer_class = PricingPlanExtendedPremiumMappingSerializer


class PricingPlanCoverMappingAPIView(ListBulkCreateUpdateDestroyAPIView):
    queryset = PricingPlanCoverMapping.objects.all()
    serializer_class = PricingPlanCoverMappingSerializer


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

            covers = PricingPlanCoverMapping.objects.filter(pricing_plan__name=pricing_plan, relationship__relative_name=dependent_type)

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

            print(f"Age: {age}")

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