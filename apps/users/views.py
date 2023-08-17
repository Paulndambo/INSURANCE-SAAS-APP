## Django Imports
from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.views import APIView


from .serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    ForgotPasswordSerializer,
)
from rest_framework import status, generics, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

## Rest Framework Imports
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.constants.utils import CustomPagination


##Serializer Imports
from .serializers import (
    MembershipSerializer,
    PolicyHolderRelativeSerializer,
    ProfileSerializer,
    UserSerializer,
    IndividualRegisterSerializer,
    PolicyHolderSerializer,
    AuthTokenCustomSerializer
)

## Model Imports
from apps.users.models import (
    User,
    Membership,
    Profile,
    PolicyHolder,
    PolicyHolderRelative,
)


class GetAuthToken(ObtainAuthToken):
    """
    ---
    POST:
        serializer: AuthTokenSerializer
    """
    serializer_class = AuthTokenCustomSerializer
    permission_classes = [AllowAny]

    def get_serializer(self):
        return self.serializer_class()

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user).key

        # Update last_login of the current user
        user.last_login = timezone.now()
        user.save()

        response = {
            'token': token,
            'pk': user.pk,
            'role': user.role,
            "username": user.username,
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}"
            #'view_id': user.get_view_id,
        }

        return Response(response)


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
    permission_classes = [AllowAny]

    def get_queryset(self):
        scheme_group = self.request.query_params.get("scheme_group")
        policy = self.request.query_params.get("policy")
        
        if scheme_group and policy:
            return self.queryset.filter(policy=policy, scheme_group_id=scheme_group)
        elif scheme_group:
            return self.queryset.filter(scheme_group_id=scheme_group)
        else:
            return self.queryset



class ProfileModelViewSet(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class PolicyHolderViewSet(ModelViewSet):
    queryset = PolicyHolder.objects.all()
    serializer_class = PolicyHolderSerializer


class PolicyHolderRelativeViewSet(ModelViewSet):
    pagination_class = CustomPagination
    queryset = PolicyHolderRelative.objects.all()
    serializer_class = PolicyHolderRelativeSerializer

    def get_queryset(self):
        dependent_type = self.request.query_params.get("dependent_type")
        if dependent_type:
            if dependent_type.lower() == "dependent":
                return self.queryset.filter(use_type__in=["Dependent", "dependent"])
            elif dependent_type.lower() == "extended":
                return self.queryset.filter(use_type__in=["extended", "Extended"])
            elif dependent_type.lower() == "beneficiary":
                return self.queryset.exclude(use_type__in=["Beneficiary", "beneficiary"])
        else:
            return self.queryset