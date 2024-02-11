import uuid
import datetime

import gevent

from celery_app import app
from models import (
    Reminder,
)


@app.task
def exec_reminder(reminder: Reminder) -> ...:

    def _finalize_reminder(reminder_id: uuid.UUID) -> None:
        ...

        # TODO load fresh reminder instance from db
        # TODO dispatch the reminder
        # TODO delete the reminder from db

    def _start_off_reminder(wait_until: datetime.datetime) -> None:
        wait_time_sec = (wait_until - datetime.datetime.now()).total_seconds()
        gevent.sleep(seconds=wait_time_sec)

    _start_off_reminder(wait_until=reminder.time)
    _finalize_reminder(reminder_id=reminder.id)
    