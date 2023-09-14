from django.db import models

from apps.constants.choice_constants import GENDER_CHOICES
from apps.core.models import AbstractBaseModel

PET_TYPES = (
    ("cat", "Cat"),
    ("dog", "Dog"),
)

PET_SIZE_CHOICES = (
    ("small", "Small"),
    ("medium", "Medium"),
    ("large", "Large"),
)


# Create your models here.
class PetBreed(AbstractBaseModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Pet(AbstractBaseModel):
    breed = models.ForeignKey(PetBreed, on_delete=models.SET_NULL, null=True)
    pet_type = models.CharField(max_length=255, choices=PET_TYPES)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    color = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255, choices=PET_SIZE_CHOICES)
    description = models.TextField(null=True)
    date_of_birth = models.DateField()
    policy = models.ForeignKey("policies.Policy", on_delete=models.SET_NULL, null=True)
    scheme_group = models.ForeignKey("schemes.SchemeGroup", on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey("users.Profile", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name