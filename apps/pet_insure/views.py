from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from apps.pet_insure.models import Pet, PetBreed
from apps.pet_insure.serializers import BreedSerializer, PetSerializer


# Create your views here.
class BreedViewSet(ModelViewSet):
    queryset = PetBreed.objects.all()
    serializer_class = BreedSerializer


class PetViewSet(ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer