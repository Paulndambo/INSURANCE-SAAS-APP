from backend.celery import app
from apps.sales.models import TemporaryMemberData
from apps.sales.mixins import BulkMembersOnboardingMixin


@app.task(name="print_hello_world")
def print_hello_world():
    members = TemporaryMemberData.objects.filter(processed=True)
    data = [
        {
            "id": 1,
            "name": "John Doe",
            "profession": "Software Developer"
        },
        {
            "id": 2,
            "name": "Jane Doe",
            "profession": "DevOps Engineer"
        }
    ]

    if members.count() > 1:
        bulk_mixin = BulkMembersOnboardingMixin(members)
        bulk_mixin.run()
    else:
        print("*******************************All Members Have Been Processed!*********************************")


app.conf.beat_schedule = {
    'run-every-2-seconds': {
        'task': 'print_hello_world',
        'schedule': 2
    }
}
