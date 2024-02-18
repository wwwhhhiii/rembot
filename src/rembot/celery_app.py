from celery import Celery

from messaging_settings import messaging_settings


app = Celery(
    'reminders',
    broker=messaging_settings.broker_connection_string,
    backend="rpc://")
