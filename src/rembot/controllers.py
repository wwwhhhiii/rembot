import uuid

from src.rembot.tasks import exec_reminder
from src.rembot.models import (
    Reminder,
    ReminderCreateRequest,
    ReminderGetRequest,
    ReminderUpdateRequest,
    ReminderDeleteRequest,
)


def create_reminder(request: ReminderCreateRequest) -> ...:
    """"""

    reminder = Reminder(
        id=uuid.uuid4(),
        username=request.username,
        time=request.time,
        text=request.text)
    
    # TODO add to db

    res = exec_reminder.delay(reminder)

    # TODO return status


def get_reminder(request: ReminderGetRequest) -> ...:
    """"""

    # TODO get reminder by id
    request.reminder_id

    # TODO return success status


def get_user_reminders(username: str) -> ...:
    """"""

    # TODO return paginated reminders


def update_reminder(request: ReminderUpdateRequest) -> ...:
    """"""

    # TODO load reminder from db, check if exists
    reminder = ...
    if reminder is None:
        ...  # TODO return does not exist status

    # TODO if updated text -> update text in db
    # TODO if updated time -> update time in db -> delete worker, start worker with new time
    res = exec_reminder.delay(reminder)

    # TODO return success status


def delete_reminder(request: ReminderDeleteRequest) -> ...:
    """"""

    # TODO load reminder from db, check if exists
    # TODO stop worker, delete reminder from db 
