import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token

from apps.constants.choice_constants import (GENDER_CHOICES, ROLE_CHOICES,
                                             SUB_ROLE_CHOICES)
from apps.constants.premium_methods import get_same_date_next_month
from apps.core.models import AbstractBaseModel


class User(AbstractUser, AbstractBaseModel):
    PASSWORD_EXPIRATION_DAYS = 90

    token = models.CharField(null=True, max_length=255)
    token_expiration_date = models.DateTimeField(null=True)
    activation_date = models.DateTimeField(null=True)
    email = models.EmailField(
        unique=True,
        error_messages={"unique": _("A user with that email already exists.")},
    )
    role = models.CharField(choices=ROLE_CHOICES, max_length=32)
    image = models.ImageField(upload_to="user_images/", null=True)
    sent_emails = models.IntegerField(default=0)
    password_expiration_date = models.DateField(null=True)
    reset_password = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    

MARITAL_STATUS_CHOICES = (
    ("single", "Single"),
    ("married", "Married"),
    ("divorced", "Divorced"),
    ("widowed", "Widowed"),
)

MEMBERSHIP_STATUS_CHOICES = (
    ("draft", "Draft"),
    ("created", "Created"),
    ("active", "Active"),
    ("cancelled", "Cancelled"),
)


class Membership(AbstractBaseModel):
    member_id = models.UUIDField(default=uuid.uuid4, unique=True)
    description = models.TextField(null=True)
    #price_request = models.ForeignKey('generic_policy_prices.PolicyPriceRequest', null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    scheme_group = models.ForeignKey('schemes.SchemeGroup', on_delete=models.CASCADE, related_name="schemegroupmembers")
    policy = models.ForeignKey('policies.Policy', null=True, on_delete=models.CASCADE)
    membership_status = models.CharField(max_length=255, choices=MEMBERSHIP_STATUS_CHOICES, null=True, blank=True)
    membership_certificate = models.FileField(upload_to="membership_certificates", null=True, blank=True)
    membership_certificate_generated = models.BooleanField(default=False)
    membership_welcome_letter = models.FileField(upload_to="membership_welcome_letters/", null=True, blank=True)
    membership_premium = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    properties = models.JSONField(default=dict)

    def __str__(self):
        return self.user.username

    
    def get_profile(self):
        user = self.user
        profile = Profile.objects.filter(user=user).first()
        if profile:
            user_profile = {
                "name": f"{profile.first_name} {profile.last_name}",
                "phone_number": profile.phone_number,
                "postal_address": profile.postal_address,
                "physical_address": profile.physical_address,
                "id_number": profile.id_number,
                "date_of_birth": profile.date_of_birth,
                "gender": profile.gender,
                "occupation": profile.occupation,
                "nationality": profile.nationality,
                "identification_method": 1 if profile.id_number else 0
            }
            return user_profile
        
    def get_membership_configuration(self):
        membership_config = self.membershipconfigs.filter(beneficiary__isnull=True).values().first()
        if membership_config:
            return membership_config
        else:
            return None

    def raise_new_policy_premium(self):
        latest_premium = self.membershipprems.order_by("-expected_date").first()

        if latest_premium:
            next_expected_date = get_same_date_next_month(latest_premium.expected_date)
            next_premium_amount = latest_premium.expected_payment
            next_balance = -abs(latest_premium.balance - next_premium_amount)

            new_reference = latest_premium.reference + 1

            new_premium = self.membershipprems.create(
                policy=latest_premium.policy,
                membership=latest_premium.membership,
                amount_paid=0,
                expected_payment=next_premium_amount,
                expected_date=next_expected_date,
                balance=next_balance,
                status="future",
                reference=new_reference
            )

            #new_premium = PolicyPremium.objects.create(
            #    policy=latest_premium.policy,
            #    membership=latest_premium.membership,
            #    amount_paid=0,
            #    expected_payment=next_premium_amount,
            #    expected_date=next_expected_date,
            #    balance=next_balance,
            #    status="future"
            #)
            
            print(f"Premium: {new_premium.id} Expected On: {new_premium.expected_date} Created Successfully!!")


class MembershipConfiguration(AbstractBaseModel):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name="membershipconfigs")
    beneficiary = models.ForeignKey("dependents.Beneficiary", on_delete=models.CASCADE, blank=True, null=True)
    pricing_plan = models.ForeignKey("prices.PricingPlan", on_delete=models.SET_NULL, null=True, blank=True)
    cover_level = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.membership.user.email


class MembershipStatusUpdates(AbstractBaseModel):
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=255)
    next_status = models.CharField(max_length=255)

    def __str__(self):
        return self.membership.user.username


class Profile(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profiles")
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    id_number = models.CharField(max_length=255, null=True, unique=True)
    date_of_birth = models.DateField(null=True)
    occupation = models.TextField(null=True)
    nationality = models.CharField(max_length=120, null=True)
    gender = models.CharField(null=True, max_length=60, choices=GENDER_CHOICES)
    physical_address = models.CharField(max_length=255, null=True, blank=True)
    postal_address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    work_phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PolicyHolder(AbstractBaseModel):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name="policyholders")
    name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    id_number = models.CharField(max_length=255, null=True, unique=True)
    date_of_birth = models.DateField(null=True)
    gender = models.CharField(null=True, max_length=60)
    occupation = models.TextField(null=True)
    nationality = models.CharField(max_length=120, null=True)
    gender = models.CharField(null=True, max_length=60, choices=GENDER_CHOICES)
    physical_address = models.CharField(max_length=255, null=True, blank=True)
    postal_address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    work_phone = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.id_number


class PolicyHolderRelative(AbstractBaseModel):
    USE_TYPES = (
        ("main_member", "Main Member"),
        ("dependent", "Dependent"),
        ("beneficiary", "Beneficiary"),
        ("parents", "Parents"),
        ("stillborn", "Stillborn"),
        ("extended", "Extended"),
    )

    relative_name = models.CharField(max_length=255)
    relative_key = models.CharField(max_length=255, unique=True)
    degree_of_separation = models.IntegerField()
    use_type = models.CharField(max_length=128, choices=USE_TYPES, default="dependent")


    def __str__(self):
        return self.relative_name
    