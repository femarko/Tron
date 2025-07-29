from dataclasses import (
    dataclass,
    field
)
import os
from dotenv import load_dotenv

load_dotenv()


#
#
# env_values = dotenv_values(os.getenv("ENV_FILE", ".env"))
#
# @dataclasses.dataclass
# class Config:
#     db_url = (f"postgresql://{env_values.get('POSTGRES_USER', dotenv_values('.env.dev').get('POSTGRES_USER'))}:"
#               f"{env_values.get('POSTGRES_PASSWORD', dotenv_values('.env.dev').get('POSTGRES_PASSWORD'))}@"
#               f"{env_values.get('POSTGRES_HOST', dotenv_values('.env.dev').get('POSTGRES_HOST'))}:"
#               f"{env_values.get('POSTGRES_PORT', dotenv_values('.env.dev').get('POSTGRES_PORT'))}/"
#               f"{env_values.get('POSTGRES_DB', dotenv_values('.env.dev').get('POSTGRES_DB'))}")
#     mode = env_values.get("MODE", dotenv_values(".env.dev").get("MODE"))
#
#
# settings = Config()


@dataclass
class Config:
    """
    Application configuration holder.

    Loads environment variables and assembles a PostgreSQL connection string
    depending on the current runtime mode. This configuration is meant to be
    instantiated once at startup and used throughout the application.

    Attributes
    ----------
    mode : str
        The runtime mode of the application. Can be "prod", "test" or "dev".
    db_url : str
        Fully constructed PostgreSQL connection URL.
    """
    mode: str = field(default_factory=lambda: os.getenv("MODE", "prod"))
    db_url: str = field(init=False)

    def __post_init__(self):
        """
        Builds the database URL from environment variables after initialization.
        """

        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT")
        database = os.getenv("POSTGRES_DB")

        if not all([user, password, host, port, database]):
            missing = [name for name, value in [
                ("POSTGRES_USER", user),
                ("POSTGRES_PASSWORD", password),
                ("POSTGRES_HOST", host),
                ("POSTGRES_PORT", port),
                ("POSTGRES_DB", database),
            ] if not value]
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")
        self.db_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"

settings = Config()