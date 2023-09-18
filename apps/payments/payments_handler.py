from datetime import date
from decimal import Decimal

from apps.payments.models import PolicyPayment, PolicyPremium
from apps.policies.models import Policy
from apps.schemes.models import SchemeGroup
from apps.users.models import Membership, Profile


class DynamicPaymentsHandlingMixin(object):
    def __init__(self, policy_number: str, amount_paid: Decimal , payment_date: date, id_number: str):
        self.policy_number = policy_number
        self.amount_paid = amount_paid
        self.payment_date = payment_date
        self.id_number = id_number


    def run(self):
        self.__dynamic_payments_handling()


    @classmethod
    def premium_multiple_checker(cls, dividend, divisor):
        multiple_times = dividend / divisor
        return multiple_times

    def __dynamic_payments_handling(self):
        # Check how many times the paid amount goes into the premium
        """
        1. Member/PolicyHolder Identification
        """
        policy = Policy.objects.get(policy_number=self.policy_number)
        profile = Profile.objects.get(id_number=self.id_number)
        membership = Membership.objects.get(policy=policy, user=profile.user)

        """
        2. Member/PolicyHolder Premiums
        """
        membership_premium = membership.membership_premium
        premium_payment_comparison = self.premium_multiple_checker(self.amount_paid, membership_premium)
        
        print(premium_payment_comparison)
        
