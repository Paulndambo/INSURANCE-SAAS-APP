from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.prices.medical.serializers import GeneralMedicalPricingSerializer


class GeneralMedicalCoverAPIView(generics.CreateAPIView):
    serializer_class = GeneralMedicalPricingSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        age_group = 
        spouse_covered = 
        spouse_age_group = 
        children_covered = 
        number_of_children = 
        inpatient_cover = 
        outpatient_cover = 
        """
        data = request.data

        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
