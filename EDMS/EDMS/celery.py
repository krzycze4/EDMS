import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EDMS.settings")

app = Celery("EDMS")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.beat_schedule = {
    "set_agreement_is_current_every_day_at_midnight": {
        "task": "employees.tasks.set_agreement_is_current",
        "schedule": crontab(hour=0, minute=0),
    },
    "set_user_is_active_to_false_every_day": {
        "task": "employees.tasks.set_user_is_active_to_false",
        "schedule": crontab(hour=0, minute=5),
    },
    "add_new_vacation_in_new_year": {
        "task": "employees.tasks.set_user_vacation_left",
        "schedule": crontab(hour=0, minute=10, day_of_month="1", month_of_year="1"),
    },
}

app.autodiscover_tasks()
