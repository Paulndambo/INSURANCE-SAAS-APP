from rest_framework import serializers

from apps.pet_insure.models import Pet, PetBreed


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PetBreed
        fields = "__all__"


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"