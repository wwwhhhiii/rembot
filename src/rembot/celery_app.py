from celery import Celery

from settings.messaging import messaging_settings


app = Celery(
    'reminders',
    broker=messaging_settings.broker_connection_string,
    backend="rpc://")
