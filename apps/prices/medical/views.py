from decimal import Decimal

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.prices.medical.serializers import (GeneralMedicalPricingSerializer,
                                             MedicalCoverSerializer)
from apps.prices.models import MedicalCover, MedicalCoverPricing


class MedicalCoverAPIView(generics.ListAPIView):
    queryset = MedicalCover.objects.all()
    serializer_class = MedicalCoverSerializer

    def get(self, *args, **kwargs):
        pricing_plan = self.request.query_params.get("pricing_plan")

        if pricing_plan:
            covers = MedicalCover.objects.filter(
                pricing_plan__name=pricing_plan).first()
            serializer = self.serializer_class(instance=covers)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Please supply a pricing plan to get values"}, status=status.HTTP_200_OK)



class GeneralMedicalCoverAPIView(generics.CreateAPIView):
    serializer_class = GeneralMedicalPricingSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        cover_name = self.request.query_params.get("cover_name")
        if not cover_name:
            return Response({"failed": "Please make sure to pass cover_name as a query param"}, status=status.HTTP_400_BAD_REQUEST)
        
        medical_cover = MedicalCover.objects.get(name=cover_name)
        
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            ph_age_group = data.get("ph_age_group")
            spouse_covered = data.get("spouse_covered")
            spouse_age_group = data.get("spouse_age_group")
            children_covered = data.get("children_covered")
            number_of_children = data.get("number_of_children")
            inpatient_cover = data.get("inpatient_cover")
            outpatient_cover = data.get("outpatient_cover")

            if spouse_covered and children_covered:
                inpatient_cover = Decimal(inpatient_cover)
                outpatient_cover = Decimal(outpatient_cover)

                pricing = MedicalCoverPricing.objects.filter(
                    medical_cover=medical_cover,
                    outpatient_cover=outpatient_cover,
                    inpatient_cover=inpatient_cover,
                    ph_age_group=ph_age_group,
                    spouse_age_group=spouse_age_group
                ).first()
                if pricing:
                    return Response({
                        "premium_per_month": pricing.ph_premium + pricing.spouse_premium + (pricing.child_premium * number_of_children),
                        "premium_per_year": (pricing.ph_premium + pricing.spouse_premium + (pricing.child_premium * number_of_children)) * 12
                    })
                return Response({}, status=status.HTTP_200_OK)

            elif spouse_covered and not children_covered:
                inpatient_cover = Decimal(inpatient_cover)
                outpatient_cover = Decimal(outpatient_cover)

                pricing = MedicalCoverPricing.objects.filter(
                    medical_cover=medical_cover,
                    outpatient_cover=outpatient_cover,
                    inpatient_cover=inpatient_cover,
                    ph_age_group=ph_age_group,
                    spouse_age_group=spouse_age_group
                ).first()

                if pricing:
                    return Response({
                        "premium_per_month": pricing.ph_premium + pricing.spouse_premium,
                        "premium_per_year": (pricing.ph_premium + pricing.spouse_premium) * 12
                    })
                return Response({}, status=status.HTTP_200_OK)

            elif children_covered and not spouse_covered:
                inpatient_cover = Decimal(inpatient_cover)
                outpatient_cover = Decimal(outpatient_cover)

                pricing = MedicalCoverPricing.objects.filter(
                    medical_cover=medical_cover,
                    outpatient_cover=outpatient_cover,
                    inpatient_cover=inpatient_cover,
                    ph_age_group=ph_age_group
                ).first()

                if pricing:
                    return Response({
                        "premium_per_month": pricing.ph_premium + (pricing.child_premium * number_of_children),
                        "premium_per_year": (pricing.ph_premium + (pricing.child_premium * number_of_children)) * 12
                    })
                return Response({}, status=status.HTTP_200_OK)

            return Response({}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
