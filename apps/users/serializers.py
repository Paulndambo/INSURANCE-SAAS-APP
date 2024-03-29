import datetime

from django.contrib.auth import authenticate
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.exceptions import AuthenticationFailed

from apps.constants.token_generator import generate_unique_key
from apps.users.models import (Membership, MembershipConfiguration,
                               PolicyHolder, PolicyHolderRelative, Profile,
                               User)


from rest_framework_bulk import (
    BulkSerializerMixin,
)

class PolicyHolderRelativeMappingSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    class Meta(object):
        model = PolicyHolderRelative
        fields = "__all__"

class AuthTokenCustomSerializer(AuthTokenSerializer):

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                # From Django 1.10 onwards the `authenticate` call simply
                # returns `None` for is_active=False users.
                # (Assuming the default `ModelBackend` authentication backend.)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _('Unable to log in with provided credentials.')
                raise AuthenticationFailed(msg, code='authorization')
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs

        

class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ("id", "name", "username", "email", "role")
    
    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


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
    profile = serializers.ReadOnlyField(source="get_profile")
    membership_config = serializers.ReadOnlyField(source="get_membership_configuration")
    status = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    class Meta:
        model = Membership
        fields = "__all__"

    def get_status(self, obj):
        cycle = obj.cycles.first()
        return cycle.status

    def get_email(self, obj):
        return obj.user.email

    """
    def create(self, validated_data):
        try:
            membership = Membership.objects.create(**validated_data)
            MembershipConfiguration.objects.create(
                membership=membership,
                cover_level=50000,
                pricing_plan=membership.scheme_group.pricing_group
            )
            return membership
        except Exception as e:
            raise e
    """

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
