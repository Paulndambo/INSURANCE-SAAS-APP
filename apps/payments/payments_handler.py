import json
from decimal import Decimal

from django.db import transaction

from apps.constants.csv_to_json_processor import csv_to_json
from apps.payments.models import PaymentLog, PolicyPayment
from apps.policies.models import Policy
from apps.users.models import Membership, Profile


class DynamicPaymentsHandlingMixin(object):
    def __init__(self, data):
        self.data = data

    def run(self):
        self.__dynamic_payments_handling()

    @classmethod
    def get_membership(cls, policy_number, id_number):
        policy = Policy.objects.filter(policy_number=policy_number).first()
        profile = Profile.objects.filter(id_number=id_number).first()

        membership = Membership.objects.filter(policy=policy, user=profile.user).first()

        return membership, policy

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
    def record_multiple_manual_payments(cls, payment_data):
        payments_list = []
        for payment in payment_data:
            policy_number = payment.get("policy_number")
            amount = Decimal(payment.get("amount"))
            id_number = payment.get("id_number")
            payment_date = payment.get("payment_date")
            membership, policy = cls.get_membership(policy_number, id_number)

            payments_list.append(PaymentLog(
                id_number=id_number,
                policy=policy,
                membership=membership,
                amount=amount,
                payment_date=payment_date,
                payment_type="manual",
                processed=False,
                balance=amount
            ))

        if payments_list:
            PaymentLog.objects.bulk_create(payments_list)

    @classmethod
    def record_single_manual_payment(cls, policy_number, id_number, payment_date, amount):
        membership, policy = cls.get_membership(policy_number, id_number)

        PaymentLog.objects.create(
            id_number=id_number,
            policy=policy,
            membership=membership,
            payment_date=payment_date,
            payment_type="manual",
            amount=amount,
            processed=False,
            balance=amount
        )

    def __dynamic_payments_handling(self):
        policy_number = self.data.get("policy_number")
        id_number = self.data.get("id_number")
        payment_date = self.data.get("payment_date")
        payment_type = self.data.get("payment_type")
        payment_data = self.data.get("payment_data")
        amount = self.data.get("amount")

        if payment_type == "multiple":
            data = csv_to_json(payment_data)
            statements_data = json.loads(data)

            self.record_multiple_manual_payments(statements_data)

        else:
            self.record_single_manual_payment(policy_number, id_number, payment_date, amount)
