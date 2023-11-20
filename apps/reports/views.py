from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.reports.serializers import PolicyHolderReportSerializer
from apps.users.models import Membership

from .utils import (get_all_cards, get_card_data, get_databases,
                    get_metabase_token)


# Create your views here.
class PolicyHolderReportViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = PolicyHolderReportSerializer



class MetabasePolicyHolderAPIView(APIView):
    def get(self, request, *args, **kwargs):
        token = get_metabase_token()
        print(f"Token: {token}")
        data = get_card_data(token, 9)
        return Response(data)


class GeneralAnalyticsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        analytics = {
            "users": 59,
            "policies_purchased_today": 56,
            "policies_purchased_this_month": 7000,
            "premiums_collections": 5400000,
            "missed_premiums_collections": 65000 
        }
        return Response(analytics, status=status.HTTP_200_OK)