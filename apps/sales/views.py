from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from apps.sales.data_construction_methods import (
    new_member_data_constructor,
    new_family_member_data_constructor
)


# from apps.policies.mixins import CancelIndividualPolicyMixin, BulkMemberUploadMixin, SchemeGroupPolicyCancellationMixin

from apps.sales.serializers import (
    BulkTemporaryPaidMemberDataBulkSerializer,
    BulkTemporaryMemberCancellationUploadSerializer,
    BulkTemporaryDependentUploadSerializer,
    BulkTemporaryNewMemberUploadSerializer,
    TemporaryDataHoldingSerializer,
    FailedUploadDataSerializer,
    BulkTemporaryMemberDataSerializer,
    NewMembersSerializer,
    TelesalesBulkTemporaryMemberDataSerializer
)
# from apps.sales.useful_methods import bulk_policy_upload
from apps.sales.models import (
    FailedUploadData, 
    TemporaryDataHolding, 
    TemporaryMemberData,
    TemporaryDependentImport
)
from rest_framework_bulk import (
    BulkListSerializer,
    BulkSerializerMixin,
    ListBulkCreateUpdateDestroyAPIView,
)

from apps.sales.tasks import onboard_family_members, mark_members_as_paid_task, mark_members_as_cancelled, onboard_new_members_task

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


class BulkTemporaryMemberDataAPIView(generics.ListCreateAPIView):
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
        upload_data = request.data.get("upload_data")
        upload_type = request.data.get("upload_type")
        onboarding_mode = request.data.get('onboarding_mode')

        if onboarding_mode and upload_type and upload_data:
            data = {
                "upload_type": "paid_members",
                "upload_data": upload_data,
                "onboarding_mode": "background"
            }

            serializer = TemporaryDataHoldingSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                x = serializer.save()
                print(x.id)
                try:
                    mark_members_as_paid_task()
                except Exception as e:
                    raise e
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    "message": f"Please make sure your request body contains, upload_type: str, onboarding_model: str, upload_data: list"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


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
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        upload_data = request.data.get("upload_data")
        upload_type = request.data.get("upload_type")
        onboarding_mode = request.data.get('onboarding_mode')

        if onboarding_mode and upload_type and upload_data:
            data = {
                "upload_type": "cancelled_members",
                "upload_data": upload_data,
                "onboarding_mode": "background"
            }

            serializer = TemporaryDataHoldingSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                x = serializer.save()
                print(x.id)
                try:
                    mark_members_as_cancelled()
                except Exception as e:
                    raise e
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    "message": f"Please make sure your request body contains, upload_type: str, onboarding_model: str, upload_data: list"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class BulkTemporaryNewMemberUploadAPIView(generics.CreateAPIView):
    # queryset = TemporaryMemberData.objects.all()
    serializer_class = BulkTemporaryNewMemberUploadSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        upload_data = request.data.get("upload_data")
        upload_type = request.data.get("upload_type")
        onboarding_mode = request.data.get('onboarding_mode')

        if onboarding_mode and upload_type and upload_data:
            data = {
                "upload_type": "new_members",
                "upload_data": upload_data,
                "onboarding_mode": "background"
            }

            serializer = TemporaryDataHoldingSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                x = serializer.save()
                print(x.id)
                try:
                    onboard_new_members_task()
                except Exception as e:
                    raise e
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {
                    "message": f"Please make sure your request body contains, upload_type: str, onboarding_model: str, upload_data: list"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class TemporaryDataHoldingAPIView(generics.ListCreateAPIView):
    queryset = TemporaryDataHolding.objects.all()
    serializer_class = TemporaryDataHoldingSerializer
    permission_classes = [IsAuthenticated]


class FailedUploadDataAPIView(generics.ListAPIView):
    queryset = FailedUploadData.objects.all()
    serializer_class = FailedUploadDataSerializer
    permission_classes = [IsAuthenticated]
