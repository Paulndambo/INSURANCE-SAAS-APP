from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from apps.users.models import Membership


from apps.reports.serializers import (
    PolicyHolderReportSerializer
)
# Create your views here.
class PolicyHolderReportViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = PolicyHolderReportSerializer