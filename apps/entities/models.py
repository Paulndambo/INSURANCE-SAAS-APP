from django.db import models
from django.conf import settings
from apps.core.models import AbstractBaseModel
# Create your models here.
BROKER_TYPE_CHOICES = (
    ("individual", "Individual"),
    ("entity", "Entity"),
    ("internal", "Internal"),
)

class Brokerage(AbstractBaseModel):
    name = models.CharField(max_length=255, null=True)
    website = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    broker_type = models.CharField(max_length=255, choices=BROKER_TYPE_CHOICES)
    contact_person = models.JSONField(null=True)
    postal_address = models.CharField(max_length=255, null=True)
    physical_address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class SalesAgent(AbstractBaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    broker = models.ForeignKey(Brokerage, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=255, null=True)
    postal_address = models.CharField(max_length=255, null=True)
    physical_address = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user