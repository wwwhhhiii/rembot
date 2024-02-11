from pydantic import BaseModel


class MessagingSettings(BaseModel):
    broker_connection_string: str


messaging_settings = MessagingSettings(
    broker_connection_string="amqp://admin:admin@127.0.0.1/",
)
