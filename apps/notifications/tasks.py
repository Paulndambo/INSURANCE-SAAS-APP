from backend.celery import app
from apps.sales.models import TemporaryMemberData, TemporaryDataHolding
from apps.sales.mixins import BulkMembersOnboardingMixin, BulkPaidMembersMixin


@app.task(name="print_hello_world")
def print_hello_world():
    members = TemporaryDataHolding.objects.filter(upload_type="new_members").first()

    if members:
        bulk_mixin = BulkMembersOnboardingMixin(members)
        bulk_mixin.run()
        # print(members.upload_data)
    else:
        print(
            "*******************************All Members Have Been Processed!*********************************"
        )

@app.task(name="mark_members_as_paid_task")
def mark_members_as_paid_task():
    paid_members = TemporaryDataHolding.objects.filter(upload_type="paid_members").first()

    if paid_members:
        paid_members_mixin = BulkPaidMembersMixin(paid_members.upload_data)
        paid_members_mixin.run()
        


app.conf.beat_schedule = {
    "run-every-2-seconds": {"task": "print_hello_world", "schedule": 2}
}
