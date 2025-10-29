import os
from celery import Celery

# Set default Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "crm.settings")

# Create the Celery app
app = Celery("crm")

# Load configuration from Django settings with CELERY_ prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Autodiscover tasks in all installed apps
app.autodiscover_tasks()

# Optional confirmation
@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
