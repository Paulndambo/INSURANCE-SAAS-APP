## Django Imports
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    MyTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
)
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

## Rest Framework Imports
from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet


##Serializer Imports
from .serializers import (
    UserTokenObtainPairSerializer,
    MembershipSerializer,
    PolicyHolderRelativeSerializer,
    ProfileSerializer,
    UserSerializer,
    IndividualRegisterSerializer,
    PolicyHolderSerializer,
)

## Model Imports
from apps.users.models import (
    User,
    Membership,
    Profile,
    PolicyHolder,
    PolicyHolderRelative,
)

from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.erros, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_serializer_class(self):
        return self.serializer_class()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.send_email()

        return Response(
            {"message": "Password reset link will be send to your email!"},
            status=status.HTTP_200_OK,
        )


class ChangePasswordAPIView(APIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_serializer_class(self):
        return self.serializer_class()

    def post(self, request, token):
        context = {"request": request, "token": token}
        serializer = self.serializer_class(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password has been successfully changed"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == "POST":
            return IndividualRegisterSerializer
        else:
            return UserSerializer


class MembershipViewSet(ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer


class ProfileModelViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class PolicyHolderViewSet(ModelViewSet):
    queryset = PolicyHolder.objects.all()
    serializer_class = PolicyHolderSerializer


class PolicyHolderRelativeSerializer(ModelViewSet):
    queryset = PolicyHolderRelative.objects.all()
    serializer_class = PolicyHolderRelativeSerializer
