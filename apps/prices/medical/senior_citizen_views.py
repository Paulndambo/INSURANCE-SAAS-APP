from decimal import Decimal

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.prices.medical.serializers import SeniorCitizenAfyaSerializer
from apps.prices.models import MedicalCover, MedicalCoverPricing


class SeniorCitizenAfyaAPIView(generics.CreateAPIView):
    serializer_class = SeniorCitizenAfyaSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data

        cover_name = self.request.query_params.get("cover_name")

        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):

            inpatient_cover = Decimal(data.get("inpatient_cover"))
            outpatient_cover = Decimal(data.get("outpatient_cover"))

            medical_cover = MedicalCover.objects.filter(name=cover_name).first()

            pricing = MedicalCoverPricing.objects.filter(
                medical_cover=medical_cover,
                inpatient_cover=inpatient_cover,
                outpatient_cover=outpatient_cover
            ).first()
            
            return Response({
                "monthly_premium": pricing.inpatient_premium + pricing.outpatient_premium,
                "yearly_premium": (pricing.inpatient_premium + pricing.outpatient_premium) * 12
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)