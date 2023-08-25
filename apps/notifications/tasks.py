from backend.celery import app
from apps.sales.models import TemporaryMemberData, TemporaryDataHolding
from apps.sales.mixins import (
    BulkMembersOnboardingMixin, 
    BulkPaidMembersMixin, 
    BulkRetailMemberOnboardingMixin, 
    BulkGroupMembersOnboardingMixin
)


@app.task(name="print_hello_world")
def print_hello_world():
    print("**************Hello World***************")

        

app.conf.beat_schedule = {
    "run-every-2-seconds": {"task": "print_hello_world", "schedule": 2},
    "run-every-3-seconds": {"task": "salimiana", "schedule": 3},
    #"run-every-600-seconds": {"task": "bulk_onboard_retail_members_task", "schedule": 600},
    #"run-every-900-seconds": {"task": "bulk_onboard_telesales_members_task", "schedule": 900},
    #"run-every-180-seconds": {"task": "bulk_onboard_group_members_task", "schedule": 180},

    ##Payments Tasks
    "track_premiums_expected_today": {"task": "track_premiums_expected_today", "schedule": 10 },
    "raise_future_premiums": {"task": "raise_future_premiums", "schedule": 20 },
}
