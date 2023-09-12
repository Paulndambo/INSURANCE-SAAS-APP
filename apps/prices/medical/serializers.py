from rest_framework import serializers


class GeneralMedicalPricingSerializer(serializers.Serializer):
    age_group = serializers.CharField(max_length=255)
    spouse_covered = serializers.BooleanField()
    spouse_age_group = serializers.CharField(max_length=255)
    children_covered = serializers.BooleanField()
    number_of_children = serializers.IntegerField(default=0)
    inpatient_cover = serializers.DecimalField(max_digits=20, decimal_places=2)
    outpatient_cover = serializers.DecimalField(max_digits=20, decimal_places=2)