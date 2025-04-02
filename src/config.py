import dataclasses
import pathlib
import dotenv

dotenv_path = pathlib.Path(__file__).parent.parent / ".env"
values = dotenv.dotenv_values(dotenv_path)


@dataclasses.dataclass
class Config:
    db_url = (f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@"
              f"{values.get('POSTGRES_HOST')}:{values.get('POSTGRES_PORT')}/{values.get('POSTGRES_DB')}")
    mode = values.get("MODE")
    tron_network = values.get("TRON_NETWORK")

settings = Config()
