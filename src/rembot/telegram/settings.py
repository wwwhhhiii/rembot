import pydantic
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv


load_dotenv()


class BotSettings(BaseSettings):  # type: ignore[misc]
    """Telegram bot settings"""

    token: str = pydantic.Field(validation_alias="telegram_bot_token")

    model_config = SettingsConfigDict(
        env_file="./.env",
        extra="ignore",
    )


bot_settings = BotSettings()
