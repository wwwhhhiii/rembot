from celery import Celery
import tzlocal

from messaging_settings import messaging_settings


POOL = "gevent"
CONCURRENCY = 500

RESULT_BACKEND = "rpc://"
TZ_NAME = tzlocal.get_localzone_name()

REMINDERS_CHECK_INTEVAL_SEC = 30 * 60


app = Celery(
    'reminders',
    broker=messaging_settings.broker_connection_string,
    backend=RESULT_BACKEND,)

app.conf.timezone = TZ_NAME
