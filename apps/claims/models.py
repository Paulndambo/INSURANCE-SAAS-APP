from django.db import models
from django.core.validators import MinValueValidator
from apps.core.models import AbstractBaseModel
from apps.users.models import User
# Create your models here.


class Claim(AbstractBaseModel):
    STATE_CHOICES = (
        ('lodged', 'Lodged'),
        ('awaiting_approval', 'Awaiting approval'),
        ('awaiting_payment', 'Awaiting payment'),
        ('closed', 'Closed'),
        ('paid', 'Paid'),
    )

    #insured_item = models.ForeignKey(InsuredItem, null=True, on_delete=models.CASCADE)
    policy = models.ForeignKey('policies.Policy', null=True, on_delete=models.CASCADE)
    status = models.CharField(max_length=32)
    state = models.CharField(max_length=32, choices=STATE_CHOICES)
    sub_status = models.CharField(max_length=32, null=True)
    reason = models.TextField()
    sub_reason = models.CharField(max_length=255, null=True)
    reference_number = models.CharField(max_length=32, unique=True)
    incident_date = models.DateField()
    incident_details = models.TextField(blank=True)
    amount = models.FloatField(null=True, validators=[MinValueValidator(limit_value=0), ])
    excess = models.FloatField(null=True, validators=[MinValueValidator(limit_value=0), ])
    maximum_indemnity = models.FloatField(null=True, validators=[MinValueValidator(limit_value=0), ])
    token = models.CharField(max_length=255, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    policy_status_when_lodged = models.CharField(max_length=255, null=True)
    proof_of_payment = models.FileField(upload_to="proof_of_payments/", null=True)
    membership = models.OneToOneField('users.Membership', on_delete=models.CASCADE, null=True)


class ClaimDocument(AbstractBaseModel):
    claim = models.ForeignKey(Claim, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=255)
    file_value = models.FileField(upload_to="claim_documents/", null=True)

    def __str__(self):
        return self.file_name
