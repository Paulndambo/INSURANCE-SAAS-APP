from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.prices.medical.junior_pricing_combos import \
    calculate_junior_cover_premium
from apps.prices.medical.serializers import JuniorAfyaSerializer


class JuniorAfyaAPIView(generics.CreateAPIView):
    serializer_class = JuniorAfyaSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):

            number_of_children = data.get("number_of_children")
            inpatient_cover = data.get("inpatient_cover")
            outpatient_cover = data.get("outpatient_cover")
            preferred_medical_provider = data.get("preferred_medical_provider")


            child_premium = calculate_junior_cover_premium(
                hospital=preferred_medical_provider,
                inpatient_cover=inpatient_cover,
                outpatient_cover=outpatient_cover
            )

            return Response({
                "premium_per_month": child_premium * int(number_of_children), 
                "premium_per_year": child_premium * int(number_of_children) * 12,
                "number_of_children": number_of_children,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)