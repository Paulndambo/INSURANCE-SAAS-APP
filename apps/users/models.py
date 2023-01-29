from django.db import models
from apps.core.models import AbstractBaseModel
from django.conf import settings

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
)

MARITAL_STATUS_CHOICES = (
    ("single", "Single"),
    ("married", "Married"),
    ("divorced", "Divorced"),
    ("widowed", "Widowed"),
)

class PolicyHolder(AbstractBaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
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