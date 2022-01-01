import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_backend_test.settings")

app = Celery("python_backend_test", broker="redis://localhost", backend="redis://localhost")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
