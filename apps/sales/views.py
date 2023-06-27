from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from apps.sales.data_construction_methods import (
    new_member_data_constructor,
    new_family_member_data_constructor,
    new_paid_member_data_constructor,
    new_cancelled_member_data_constructor
)
from apps.sales.tasks import onboard_sales_flow_member_task

# from apps.policies.mixins import CancelIndividualPolicyMixin, BulkMemberUploadMixin, SchemeGroupPolicyCancellationMixin

from apps.sales.serializers import (
    BulkTemporaryPaidMemberDataBulkSerializer,
    BulkTemporaryMemberCancellationUploadSerializer,
    BulkTemporaryDependentUploadSerializer,
    TemporaryDataHoldingSerializer,
    FailedUploadDataSerializer,
    BulkTemporaryMemberDataSerializer,
    NewMembersSerializer,
    PolicyPurchaseSerializer,
    CreditLifePolicyPurchaseSerializer
)
# from apps.sales.useful_methods import bulk_policy_upload
from apps.sales.models import (
    FailedUploadData, 
    TemporaryDataHolding, 
    TemporaryMemberData,
    TemporaryDependentImport,
    TemporaryCancelledMemberData,
    TemporaryPaidMemberData
)

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            policy_type = serializer.validated_data["policy_details"]["scheme_type"]
            if policy_type.lower() == "retail":
                members = serializer.validated_data.get("members")
                dependents = serializer.validated_data.get("dependents")
                beneficiaries = serializer.validated_data.get("beneficiaries")
                extended_dependents = serializer.validated_data.get("extended_dependents")

                print("******************Sales Flow Payload***********************")
                print(members)
                onboard_sales_flow_member_task(2, members)
                print("******************Sales Flow Payload***********************")
                print(dependents)
                print("******************Sales Flow Payload***********************")
                print(beneficiaries)
                print("******************Sales Flow Payload***********************")
                print(extended_dependents)
                print("******************Sales Flow Payload***********************")

                #onboard_sales_flow_member_task()
            elif policy_type.lower() == "group":
                print("This is a group policy")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
class CreditLifePolicyPurchaseAPIView(generics.CreateAPIView):
    serializer_class = CreditLifePolicyPurchaseSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)