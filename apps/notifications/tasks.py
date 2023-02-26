from backend.celery import app
from apps.sales.models import TemporaryMemberData


@app.task(name="print_hello_world")
def print_hello_world():
    members = TemporaryMemberData.objects.all()

    print("*****************Member Data**********************")
    print(members)
    print("*****************Member Data**********************")


app.conf.beat_schedule = {
    'run-every-2-seconds': {
        'task': 'print_hello_world',
        'schedule': 2
    }
}
