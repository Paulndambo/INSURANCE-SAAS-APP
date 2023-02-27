from backend.celery import app
from apps.sales.models import TemporaryMemberData, TemporaryDataHolding
from apps.sales.mixins import BulkMembersOnboardingMixin


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


app.conf.beat_schedule = {
    "run-every-2-seconds": {"task": "print_hello_world", "schedule": 2}
}
