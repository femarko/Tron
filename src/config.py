import dataclasses
import dotenv
import os

dotenv.load_dotenv()

@dataclasses.dataclass
class Config:
    db_url = (f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
              f"{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}")
    mode = os.getenv("MODE")
    tron_network = os.getenv("TRON_NETWORK")




settings = Config()
