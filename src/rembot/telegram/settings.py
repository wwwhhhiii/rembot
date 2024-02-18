import pydantic
import pydantic_settings as py_set
from dotenv import load_dotenv


load_dotenv()


class BotSettings(py_set.BaseSettings):
    """Telegram bot settings"""

    token: str = pydantic.Field(
        validation_alias="telegram_bot_token")

    model_config = py_set.SettingsConfigDict(
        env_file='./.env',
        extra='ignore',
    )


bot_settings = BotSettings()
