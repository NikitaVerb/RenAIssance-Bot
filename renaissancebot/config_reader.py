from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: SecretStr
    provider_token: SecretStr
    test_bot_token: SecretStr
    model_config = SettingsConfigDict(env_file='../Data/.env', env_file_encoding='utf-8')


config = Settings()