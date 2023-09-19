import json
from datetime import date
from decimal import Decimal

from django.db import connection, transaction

from apps.constants.csv_to_json_processor import csv_to_json
from apps.payments.models import PolicyPayment, PolicyPremium
from apps.policies.models import Policy
from apps.schemes.models import SchemeGroup
from apps.users.models import Membership, Profile


class DynamicPaymentsHandlingMixin(object):
    def __init__(self, data):
        self.data = data
        

    def run(self):
        self.__dynamic_payments_handling()


    @classmethod
    def premium_multiple_checker(cls, dividend, divisor):
        multiple_times = dividend / divisor
        return multiple_times

    @classmethod
    def premium_status_finder(cls, membership_premium, amount_paid):

        premium_status = ""
        if membership_premium.expected_payment == amount_paid:
            premium_status = "paid"
        elif membership_premium.expected_payment > amount_paid:
            premium_status = "partial"
        elif membership_premium.expected_payment < amount_paid:
            premium_status = "overpayment"

        return premium_status


    @classmethod
    def get_membership(cls, policy_number, id_number):
        policy = Policy.objects.get(policy_number=policy_number)
        profile = Profile.objects.get(id_number=id_number)
        membership = Membership.objects.get(policy=policy, user=profile.user)

        return membership

    @classmethod
    def create_payment_record(cls, amount, membership_premium, payment_date=None):
        PolicyPayment.objects.create(
                policy=membership_premium.policy,
                premium=membership_premium,
                state="SUCCESSFUL",
                amount=amount,
                payment_date=payment_date,
                payment_method="manual"
        )

    @classmethod
    def create_new_membership_premium_and_mark_it(cls, membership, amount, payment_date=None):
        membership_premium = membership.raise_new_policy_premium()
        
        membership_prem = membership.membershipprems.all().order_by("-expected_date").first()

        membership_prem.balance += float(amount)
        membership_prem.status = cls.premium_status_finder(membership_prem, amount)
        membership_prem.amount_paid += float(amount)
        membership_prem.save()
        membership.raise_new_policy_premium()

        cls.create_payment_record(amount, membership_prem, payment_date)


    @classmethod
    def single_payment_handler(cls, amount, membership, premium = None, payment_date = None):
        with transaction.atomic():
            membership_premium = membership.membershipprems.filter(status__in=["unpaid", "pending", "future", "partial"]).order_by("expected_date").first()

            if premium:
                membership_premium = membership.membershipprems.get(id=premium)
            
            if membership_premium:
                membership_premium.amount_paid += float(amount)
                membership_premium.balance += float(amount)
                membership_premium.status = cls.premium_status_finder(membership_premium, amount)
                membership_premium.save()
                cls.create_payment_record(amount, membership_premium, payment_date)
                membership.raise_new_policy_premium()
            else:
                cls.create_new_membership_premium_and_mark_it(membership, amount, payment_date)
           

    @classmethod
    def multiple_payments_handler(cls, payments_data):
        try:
            for payment in payments_data:
                policy_number = payment.get("policy_number")
                amount = Decimal(payment.get("amount"))
                id_number = payment.get("id_number")
                payment_date = payment.get("payment_date")

                membership = cls.get_membership(policy_number, id_number)

                if membership:
                    cls.single_payment_handler(amount, membership, premium=None, payment_date=payment_date)

        except Exception as e:
            raise e
    
    def __dynamic_payments_handling(self):
        # Values
        policy_number = self.data.get("policy_number")
        id_number = self.data.get("id_number")
        payment_date = self.data.get("payment_date")
        payment_type = self.data.get("payment_type")
        premium = self.data.get("premium")
        payment_data = self.data.get("payment_data")

        """
        1. Member/PolicyHolder Identification
        """


        """
        2. Member/PolicyHolder Premiums, Always pay the oldest unpaid premium
        """
        #oldest_premium = membership.membershipprems.filter(status__in=["unpaid", "pending"]).order_by("expected_date").first()

        if payment_type == "multiple":
            data = csv_to_json(payment_data)
            statements_data = json.loads(data)
            self.multiple_payments_handler(statements_data)

        #else:
        #    policy = Policy.objects.get(policy_number=self.policy_number)
        #    profile = Profile.objects.get(id_number=self.id_number)
        #    membership = Membership.objects.get(policy=policy, user=profile.user)
        #    self.single_payment_handler(self.amount_paid, membership, self.premium)
        

        #print(f"Policy: {oldest_premium.policy.policy_number}, Amount: {oldest_premium.expected_payment}, Expected Date: {oldest_premium.expected_date}, Status: {oldest_premium.status}")
        
