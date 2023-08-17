from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView
from apps.sales.share_data_upload_methods.data_construction_methods import (
    new_member_data_constructor,
    new_family_member_data_constructor,
    new_paid_member_data_constructor,
    new_cancelled_member_data_constructor
)


from apps.sales.sales_flow_methods.retail_policy_purchase import (
    SalesFlowBulkRetailMemberOnboardingMixin
)
from apps.sales.sales_flow_methods.group_policy_purchase import (
    SalesFlowBulkGroupMembersOnboardingMixin
)


from apps.sales.serializers import (
    BulkTemporaryPaidMemberDataBulkSerializer,
    BulkTemporaryMemberCancellationUploadSerializer,
    BulkTemporaryDependentUploadSerializer,
    TemporaryDataHoldingSerializer,
    FailedUploadDataSerializer,
    BulkTemporaryMemberDataSerializer,
    NewMembersSerializer,
    PolicyPurchaseSerializer,
    CreditLifePolicyPurchaseSerializer,
    RetailPolicyPurchaseSerializer
)

from apps.sales.models import (
    FailedUploadData, 
    TemporaryDataHolding, 
    TemporaryMemberData,
    TemporaryDependentImport,
    TemporaryCancelledMemberData,
    TemporaryPaidMemberData
)
from apps.users.models import User
from apps.sales.credit_life_methods.purchase_credit_life_policy import CreditLifePolicyOnboardingMixin

# Create your views here.

class OnboardingAPPAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        routes = [
            '/bulk-upload/new-members',
            '/bulk-upload/members-cancellation',
            '/bulk-upload/paid-members',
            '/bulk-upload/lapsed-members'
        ]
        return Response(routes)


class BulkTemporaryNewMemberUploadAPIView(generics.ListCreateAPIView):
    serializer_class = BulkTemporaryMemberDataSerializer

    def post(self, request, *args, **kwargs):
        try:
            upload_data = request.data["upload_data"]
            new_members = []
            for data in upload_data:
                new_members.append(
                    TemporaryMemberData(
                        **new_member_data_constructor(data)
                    )
                )
            TemporaryMemberData.objects.bulk_create(new_members)
        except Exception as e:
            raise e
        return Response({"message": "Data Uploaded Successfully"}, status=status.HTTP_201_CREATED)



class NewMembersAPIView(generics.ListAPIView):
    queryset = TemporaryMemberData.objects.all()
    serializer_class = NewMembersSerializer
        

class OnboardingInitiateAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        url = request.query_params.get("url")
        print(url)
        return Response({"message": "Hello World"}, status=status.HTTP_200_OK)


class BulkTemporaryPaidMemberUploadAPIView(generics.ListCreateAPIView):
    # queryset = TemporaryPaidMemberData.objects.all()
    serializer_class = BulkTemporaryPaidMemberDataBulkSerializer
    #permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            upload_data = request.data["upload_data"]
            new_paid_members = []
            for member in upload_data:
                new_paid_members.append(
                    TemporaryPaidMemberData(
                        **new_paid_member_data_constructor(member)
                    )
                )
            TemporaryPaidMemberData.objects.bulk_create(new_paid_members)
        except Exception as e:
            raise e
        return Response({"message": "Data loaded successfully, onboarding should start soon, check back on the platform"}, status=status.HTTP_201_CREATED)
        

class BulkTemporaryDependentUploadAPIView(generics.ListCreateAPIView):
    serializer_class = BulkTemporaryDependentUploadSerializer
    #permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            upload_data = request.data["upload_data"]
            new_family_members = []
            for member in upload_data:
                new_family_members.append(
                    TemporaryDependentImport(
                        **new_family_member_data_constructor(member)
                    )
                )
            TemporaryDependentImport.objects.bulk_create(new_family_members)
        except Exception as e:
            raise e 
        return Response({"message": "Data loaded successfully, onboarding should start soon, check back on the platform"}, status=status.HTTP_201_CREATED)


class BulkTemporaryCancelledMemberUploadAPIView(generics.ListCreateAPIView):
    # queryset = TemporaryCancelledMemberData.objects.all()
    serializer_class = BulkTemporaryMemberCancellationUploadSerializer
    #permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            upload_data = request.data["upload_data"]
            new_cancelled_members = []

            for member in upload_data:
                new_cancelled_members.append(
                    TemporaryCancelledMemberData(
                        **new_cancelled_member_data_constructor(member)
                    )
                )
            TemporaryCancelledMemberData.objects.bulk_create(new_cancelled_members)
        except Exception as e:
            raise e
        
        return Response({"message": "Data loaded successfully, onboarding should start soon, check on the platform later"}, status=status.HTTP_201_CREATED)

        

class TemporaryDataHoldingAPIView(generics.ListCreateAPIView):
    queryset = TemporaryDataHolding.objects.all()
    serializer_class = TemporaryDataHoldingSerializer
    permission_classes = [IsAuthenticated]


class FailedUploadDataAPIView(generics.ListAPIView):
    queryset = FailedUploadData.objects.all()
    serializer_class = FailedUploadDataSerializer
    permission_classes = [IsAuthenticated]


class PolicyPurchaseAPIView(generics.CreateAPIView):
    serializer_class = PolicyPurchaseSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            scheme_type = data.get("scheme_group")["scheme"]

            print(f"Scheme Type: {scheme_type}")

            if scheme_type.lower() == "Retail Scheme".lower():
                retail_mixin = SalesFlowBulkRetailMemberOnboardingMixin(data=serializer.validated_data)
                retail_mixin.run()
            elif scheme_type.lower() == "Group Scheme".lower():
                group_mixin = SalesFlowBulkGroupMembersOnboardingMixin(data=serializer.validated_data)
                group_mixin.run()
            elif scheme_type.lower() == "credit scheme":
                credit_life_mixin = CreditLifePolicyOnboardingMixin(data=serializer.validated_data)
                credit_life_mixin.run()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetailPolicyPurchaseAPIView(generics.CreateAPIView):
    serializer_class = RetailPolicyPurchaseSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
class CreditLifePolicyPurchaseAPIView(generics.CreateAPIView):
    serializer_class = CreditLifePolicyPurchaseSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            credit_life_mixin = CreditLifePolicyOnboardingMixin(data=serializer.validated_data)
            credit_life_mixin.run()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
