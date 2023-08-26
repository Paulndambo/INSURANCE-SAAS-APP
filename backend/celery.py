import os
from celery import Celery
from django.conf import settings

cloud_amqp = "amqps://qiqdvcyl:KPtRQ1jnfpuF7NNuAaVi9tynarNPc6XH@hummingbird.rmq.cloudamqp.com/qiqdvcyl"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend", broker=cloud_amqp)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
