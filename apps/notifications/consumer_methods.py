import json
from decimal import Decimal

from apps.payments.models import PaymentLog, PolicyPayment, PolicyPremium


class NotificationConsumer:
    body = None 

    @classmethod
    def hello_world(cls):
        print(cls.body)

    @classmethod
    def process_policy_payments(cls):
        payments_to_process = PaymentLog.objects.filter(processed=False)[:1000]

        for payment in payments_to_process:
            membership_premium = payment.membership.get_the_oldest_not_fully_paid_premium()

            if not membership_premium:
                print("Future Block Executed!!")
                membership_premium = payment.membership.get_future_premium()

            
            if membership_premium:
                payment_amount = float(payment.balance)

                membership_updated_balance = membership_premium.balance + payment_amount
                membership_premium.amount_paid += payment_amount
                membership_premium.balance += payment_amount
                
                if membership_updated_balance == 0 or membership_updated_balance == 0.0:
                    membership_premium.status = "paid"
                    payment.processed = True
                    payment.balance -= Decimal(membership_premium.expected_payment)
                    payment.save()

                elif membership_updated_balance > 1:
                    membership_premium.status = "paid"
                    payment.balance -= Decimal(membership_premium.expected_payment)
                    payment.processed = False
                    payment.save()

                elif membership_updated_balance < 0 or membership_updated_balance < 0.0:
                    membership_premium.status = "partial"
                    payment.balance -= Decimal(membership_premium.expected_payment)
                    payment.processed = True
                    payment.save()

                membership_premium.save()
                    