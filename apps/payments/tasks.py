from datetime import datetime, timedelta

from django.conf import settings

from apps.core.queue_system.publisher import BasePublisher
from apps.payments.models import (FuturePremiumTracking, PaymentLog,
                                  PolicyPremium)
from apps.policies.models import Policy
from apps.sales.share_data_upload_methods.bulk_upload_methods import \
    get_same_date_next_month
from backend.celery import app

date_today = datetime.now().date()


@app.task(name="process_policy_payments")
def process_policy_payments():
    payments_to_process = list(PaymentLog.objects.filter(processed=False).values_list("id", flat=True)[:100])

    publisher = BasePublisher(
        routing_key="process_policy_payments", 
        body={
            "payment_ids": payments_to_process
        }
    )
    publisher.run()


@app.task(name="track_premiums_expected_today")
def track_premiums_expected_today():
    premiums_already_created = list(FuturePremiumTracking.objects.filter(expected_date=date_today).values_list("membership_id", flat=True))
    premiums_expected_today = PolicyPremium.objects.exclude(membership_id__in=premiums_already_created).filter(expected_date=date_today)[:2000]

    premiums_to_track = []
    if premiums_expected_today.count() == 0:
        print("No unprocessed premiums found!!")
        return

    for premium in premiums_expected_today:
        premiums_to_track.append(
            FuturePremiumTracking(
                membership=premium.membership,
                policy=premium.policy,
                expected_amount=premium.expected_payment,
                expected_date=premium.expected_date,
                premium_balance= -abs(premium.expected_payment),
                future_expected_date=get_same_date_next_month(premium.expected_date),
                new_reference = premium.reference + 1
            )
        )
    if premiums_to_track:
        FuturePremiumTracking.objects.bulk_create(premiums_to_track)



@app.task(name="raise_future_premiums")
def raise_future_premiums():
    try:
        premiums_expected_today = FuturePremiumTracking.objects.filter(processed=False).filter(expected_date=date_today)[:1000]
        premiums_to_raise_today = []

        if premiums_expected_today.count() == 0:
            print("No premiums to raise found!!")
            return 

        for record in premiums_expected_today:
            premiums_to_raise_today.append(
                PolicyPremium(
                    membership=record.membership,
                    policy=record.policy,
                    expected_date=record.future_expected_date,
                    expected_payment=record.expected_amount,
                    balance=record.premium_balance,
                    status="future",
                    reference=record.new_reference
                )
            )
            record.processed = True
            record.save()

        if premiums_to_raise_today:
            PolicyPremium.objects.bulk_create(premiums_to_raise_today)

        else:
            print("No premiums to process")
    except Exception as e:
        raise e


def missed_payment_notification():
    eight_days_from_today = date_today + timedelta(days=8)

    missed_premiums = PolicyPremium.objects.filter(status__in=["unpaid", "pending"])

    for missed_premium in missed_premiums:
        """Get all unpaid premiums belonging to membership"""
        all_unpaid_premiums = missed_premium.membership.get_unpaid_premiums()

        print("****************************************Start of Premiums List********************************")
        for premium in all_unpaid_premiums:
            print(f"Policy: {premium.policy}, Membership: {premium.membership}, Expected Date: {premium.expected_date}")
        print("****************************************End of Premiums List********************************")