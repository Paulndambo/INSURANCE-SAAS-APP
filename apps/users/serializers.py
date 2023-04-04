from apps.users.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from apps.users.models import (
    User,
    Membership,
    PolicyHolder,
    Profile,
    PolicyHolderRelative,
)
from apps.constants.token_generator import generate_unique_key
from django.utils import timezone
import datetime


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["username"] = user.username
        # ...


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token["id"] = user.id
        return token

'''
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")

'''
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    user = None
    email = serializers.EmailField()

    def send_email(self):
        self.user.token = generate_unique_key(self.user.email)
        self.user.token_expiration_date = timezone.now() + timezone.timedelta(hours=24)
        self.user.save()

    def validate_email(self, value):
        try:
            self.user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with provided email!")


class ChangePasswordSerializer(serializers.Serializer):
    user = None

    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def save(self, validated_data):
        self.user.set_password(validated_data["password"])
        self.user.token = None
        self.user.token_expiration_date = None
        if not self.user.is_active:
            self.user.activation_date = datetime.date.today()
        self.user.is_active = True
        self.user.save()

    # def validate(self, data):

    #    self.check_valid_token()
    #    check_valid_password(data, user=self.user)

    #    return data

    def check_valid_token(self):
        try:
            self.user = User.objects.get(token=self.context["token"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Token is not valid.")
        fields = "__all__"


class IndividualRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "username", "email", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = "__all__"


class PolicyHolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyHolder
        fields = "__all__"


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class PolicyHolderRelativeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyHolderRelative
        fields = "__all__"
