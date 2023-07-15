from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import generics, status

from apps.users.models import Membership

from .utils import get_all_cards, get_card_data, get_databases, get_metabase_token


from apps.reports.serializers import (
    PolicyHolderReportSerializer
)
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