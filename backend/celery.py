# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# app = Celery('backend')

# # Load task modules from all registered Django app configs.
# app.config_from_object('django.conf:settings', namespace='CELERY')

# # Autodiscover tasks in all installed apps (including Django apps).
# app.autodiscover_tasks()

import os
from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Create a Celery instance.
app = Celery('backend')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all installed apps (including Django apps).
app.autodiscover_tasks()
