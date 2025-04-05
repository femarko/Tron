import dataclasses
import os
from  dotenv import dotenv_values


env_values = dotenv_values(os.getenv("ENV_FILE", ".env.dev"))


@dataclasses.dataclass
class Config:
    db_url = (f"postgresql://{env_values.get('POSTGRES_USER', dotenv_values('.env.dev').get('POSTGRES_USER'))}:"
              f"{env_values.get('POSTGRES_PASSWORD', dotenv_values('.env.dev').get('POSTGRES_PASSWORD'))}@"
              f"{env_values.get('POSTGRES_HOST', dotenv_values('.env.dev').get('POSTGRES_HOST'))}:"
              f"{env_values.get('POSTGRES_PORT', dotenv_values('.env.dev').get('POSTGRES_PORT'))}/"
              f"{env_values.get('POSTGRES_DB', dotenv_values('.env.dev').get('POSTGRES_DB'))}")
    mode = env_values.get("MODE", dotenv_values(".env.dev").get("MODE"))


settings = Config()
