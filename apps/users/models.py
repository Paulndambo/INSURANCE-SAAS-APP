from django.db import models
from apps.core.models import AbstractBaseModel
from django.conf import settings

from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser
import uuid

from apps.constants.choice_constants import ROLE_CHOICES, SUB_ROLE_CHOICES, GENDER_CHOICES


class User(AbstractUser, AbstractBaseModel):

    PASSWORD_EXPIRATION_DAYS = 90

    token = models.CharField(null=True, max_length=255)
    token_expiration_date = models.DateTimeField(null=True)
    activation_date = models.DateTimeField(null=True)
    email = models.EmailField(unique=True, error_messages={'unique': _('A user with that email already exists.')})
    role = models.CharField(choices=ROLE_CHOICES, max_length=32, default="individual")
    sub_role = models.CharField(choices=SUB_ROLE_CHOICES, max_length=32, null=True)
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="memberships")
    description = models.TextField(null=True, blank=True)
    scheme_group = models.ForeignKey('schemes.SchemeGroup', on_delete=models.CASCADE)
    policy = models.ForeignKey('policies.Policy', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=255, choices=MEMBERSHIP_STATUS_CHOICES)

    def __str__(self):
        return self.user.username


class Profile(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profiles")
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    id_number = models.CharField(max_length=255, null=True, unique=True)
    passport_number = models.CharField(max_length=255, null=True, unique=True)
    date_of_birth = models.DateField(null=True)
    occupation = models.CharField(max_length=255, null=True, blank=True)
    nationality = models.CharField(max_length=255, null=True)
    gender = models.CharField(max_length=255, null=True, choices=GENDER_CHOICES)
    physical_address = models.CharField(max_length=255, null=True, blank=True)
    postal_address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    home_phone_number = models.CharField(max_length=255, null=True, blank=True)
    work_phone_number = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class PolicyHolder(AbstractBaseModel):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    id_number = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    postal_address = models.CharField(max_length=255, null=True)
    physical_address = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255)
    town = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.id_number


class PolicyHolderRelative(AbstractBaseModel):
    USE_TYPES = (
        ('main_member', 'Main Member'),
        ('dependent', 'Dependent'),
        ('beneficiary', 'Beneficiary'),
        ('parents', 'Parents'),
        ('stillborn', 'Stillborn'),
    )

    relative_name = models.CharField(max_length=255)
    relative_key = models.CharField(max_length=255, unique=True)
    degree_of_separation = models.IntegerField()
    use_type = models.CharField(max_length=128, choices=USE_TYPES, default='dependent')
