import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.config.settings")

app = Celery("universitly")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")


CELERY_BROKER_URL = "amqp://guest:guest@universitly_rabbitmq:5672//"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
