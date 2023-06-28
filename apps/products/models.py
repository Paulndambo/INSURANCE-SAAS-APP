from django.db import models
from apps.core.models import Insurer

# Create your models here.
INSURANCE_TYPES = (
    ("retail", "Retail"),
    ("group", "Group"),
    ("credit", "Credit"),
    ("funeral", "Funeral"),
    ("commuter", "Commuter"),
)

PAYMENT_FREQUENCY_CHOICES = (
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("quarterly", "Quarterly"),
    ("semi_annual", "Semi-Annual"),
    ("annually", "Annually"),
)


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_type = models.CharField(max_length=255, choices=INSURANCE_TYPES)
    maximum_members_count = models.IntegerField(default=1)
    description = models.TextField(null=True, blank=True)
    insurer = models.ForeignKey(Insurer, on_delete=models.SET_NULL, null=True)
    can_be_reinstated = models.BooleanField(default=True)
    policy_wording = models.FileField(upload_to="policy_wordings/", null=True)
    disclosure_notice = models.FileField(upload_to="disclosure_notices/", null=True)
    policy_document_template = models.TextField(blank=True)
    broker_commision = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_frequency = models.CharField(max_length=255, choices=PAYMENT_FREQUENCY_CHOICES, default="monthly")

    def __str__(self):
        return self.name
