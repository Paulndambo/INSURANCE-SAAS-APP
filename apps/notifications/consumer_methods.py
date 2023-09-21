from apps.payments.models import PaymentLog, PolicyPayment, PolicyPremium


class NotificationConsumer:
    body = None 

    @classmethod
    def hello_world(cls):
        print(cls.body)

    @classmethod
    def process_policy_payments(cls):
        payment_ids = cls.body["payment_ids"]

        print(payment_ids)

        """
        payments_to_process = PaymentLog.objects.filter(id__in=payment_ids)

        for payment in payments_to_process:
            membership_premium = payment.membership.get_the_oldest_not_fully_paid_premium()

            if not membership_premium:
                membership_premium = payment.membership.get_future_premium()

            if membership_premium is None:
                pass
        """