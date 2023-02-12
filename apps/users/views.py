## Django Imports
from django.shortcuts import render

## Rest Framework Imports
from rest_framework import generics, status
from rest_framework.viewsets import ModelViewSet


##Serializer Imports
from .serializers import (
    UserTokenObtainPairSerializer, MembershipSerializer, PolicyHolderRelativeSerializer, ProfileSerializer,
    UserSerializer, IndividualRegisterSerializer, PolicyHolderSerializer
)

## Model Imports
from apps.users.models import User, Membership, Profile, PolicyHolder, PolicyHolderRelative

from rest_framework_simplejwt.views import TokenObtainPairView
# Create your views here.
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return IndividualRegisterSerializer
        else:
            return UserSerializer


class MembershipModelViewSet(ModelViewSet):
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