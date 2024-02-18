from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    connection_string: str


db_settings = DatabaseSettings(
    connection_string="postgres://admin:admin@127.0.0.1:5432/rem")
