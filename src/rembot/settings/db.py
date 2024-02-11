from pydantic import BaseModel


class DatabaseSettings(BaseModel):
    connection_string: str


db_settings = DatabaseSettings(connection_string="")  # TODO
