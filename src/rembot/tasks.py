import uuid
import datetime
from typing import Any

import gevent
from loguru import logger

from celery_app import app
from models import (
    Reminder,
)


@app.task
def exec_reminder(reminder: dict[str, Any]) -> ...:

    reminder_ = Reminder(**reminder)

    def _finalize_reminder(reminder_id: uuid.UUID) -> None:
        ...

        # TODO load fresh reminder instance from db
        # TODO dispatch the reminder
        # TODO delete the reminder from db

        logger.debug("Reminder is finalized")

    def _start_off_reminder(wait_until: datetime.datetime) -> None:
        wait_time_sec = (wait_until - datetime.datetime.now()).total_seconds()
        logger.debug(f"Waiting reminder for {wait_time_sec} sec")
        gevent.sleep(seconds=wait_time_sec)

    _start_off_reminder(wait_until=reminder_.time)
    _finalize_reminder(reminder_id=reminder_.id)
    