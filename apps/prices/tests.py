from django.test import TestCase
from apps.prices.models import PricingPlanCoverMapping, PricingPlan
# Create your tests here.
class PricingPlansTestCase(TestCase):
    def setUp(self):
        self.plan = PricingPlan.objects.create(
            name="Funeral Cover",
            base_premium=40.00,
            value_added_service=0.00,
            total_premium=40.00,
            group="group"
        )

    
    def testPricingPlanName(self):
        assert self.plan.name == "Funeral Cover"

    def testPricingPremium(self):
        assert self.plan.base_premium == 40.00
        #assert type(self.plan.base_premium) ==