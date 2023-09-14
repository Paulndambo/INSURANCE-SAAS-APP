from rest_framework import serializers


class GeneralMotorInsuranceSerializer(serializers.Serializer):
    #vehicle_type = serializers.CharField(max_length=255)
    vehicle_price = serializers.DecimalField(max_digits=20, decimal_places=2)
    year_of_manufacture = serializers.IntegerField()