from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.dependents.models import Beneficiary, Dependent
from apps.dependents.serializers import (BeneficiarySerializer,
                                         DependentSerializer)
from apps.payments.models import PaymentLog, PolicyPayment, PolicyPremium


# Create your views here.
class CustomerDependentViewSet(ModelViewSet):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        memberships = user.usermembership.all()
        return self.queryset.filter(dependent_type__in=["Dependent", "dependent"], membership__in=memberships)


class CustomerExtendedDependentViewSet(ModelViewSet):
    queryset = Dependent.objects.all()
    serializer_class = DependentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        memberships = user.usermembership.all()
        return self.queryset.filter(dependent_type__in=["extended", "Extended"], membership__in=memberships)


class CustomerBeneficiariesViewSet(ModelViewSet):
    queryset = Beneficiary.objects.all()
    serializer_class = BeneficiarySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        memberships = user.usermembership.all()
        print(memberships)
        return self.queryset.filter(membership__in=memberships)