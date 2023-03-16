from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import AbstractBaseModel
from apps.users.models import User


# Create your models here.
class Claim(AbstractBaseModel):
    STATE_CHOICES = (
        ("lodged", "Lodged"),
        ("awaiting_approval", "Awaiting approval"),
        ("awaiting_payment", "Awaiting payment"),
        ("closed", "Closed"),
        ("paid", "Paid"),
    )

    # insured_item = models.ForeignKey(InsuredItem, null=True, on_delete=models.CASCADE)
    policy = models.ForeignKey("policies.Policy", null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=32)
    sub_status = models.CharField(max_length=32, null=True)
    reason = models.TextField()
    sub_reason = models.CharField(max_length=255, null=True)
    reference_number = models.CharField(max_length=32, unique=True)
    incident_date = models.DateField()
    incident_details = models.TextField(blank=True)
    amount = models.FloatField(null=True, validators=[MinValueValidator(limit_value=0),],)
    excess = models.FloatField(null=True, validators=[MinValueValidator(limit_value=0),],)
    maximum_indemnity = models.FloatField(null=True, validators=[MinValueValidator(limit_value=0)],)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    policy_status_when_lodged = models.CharField(max_length=255, null=True)
    proof_of_payment = models.FileField(upload_to="proof_of_payments/", null=True)
    membership = models.ForeignKey("users.Membership", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.reference_number


class ClaimDocument(AbstractBaseModel):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_value = models.FileField(upload_to="claim_documents/", null=True)

    def __str__(self):
        return self.file_name


class ClaimStatusUpdates(AbstractBaseModel):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    previous_status = models.CharField(max_length=255)
    next_status = models.CharField(max_length=255)

    def __str__(self):
        return self.claim.reference_number


class ClaimAdditionalInfo(AbstractBaseModel):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    is_file = models.BooleanField(default=False)
    file = models.FileField(upload_to="claim_additional_files/", null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
