from decimal import Decimal

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.prices.motor_insure.general_motor_pricing import \
    get_motor_vehicle_policy_premium
from apps.prices.motor_insure.serializers import \
    GeneralMotorInsuranceSerializer


class GeneralMotorInsuranceAPIView(generics.CreateAPIView):
    serializer_class = GeneralMotorInsuranceSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            vehicle_price = data.get("vehicle_price")
            year_of_manufacture = data.get("year_of_manufacture")

            premium = get_motor_vehicle_policy_premium(vehicle_price, year_of_manufacture)
            monthly_premium = premium / 12
            return Response(
                {"monthly_premium": f"{monthly_premium:.2f}", 
                "yearly_premium": f"{premium:.2f}"},
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
