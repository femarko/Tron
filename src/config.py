import os
from typing import Optional

import dotenv
from dataclasses import dataclass

from src.orm_tool.sql_aclchemy_wrapper import ORMConf


dotenv.load_dotenv()


@dataclass
class Config:
    db_url: str
    tron_network: Optional[str] = None

def load_config(mode: str) -> Config:
    match mode:
        case "test":
            db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:"\
                     f"{os.getenv('POSTGRES_TEST_PASSWORD')}@"\
                     f"{os.getenv('POSTGRES_HOST')}:"\
                     f"{os.getenv('POSTGRES_TEST_PORT')}/"\
                     f"{os.getenv('POSTGRES_TEST_DB')}"
            tron_network = "nile"
            config = Config(db_url=db_url, tron_network=tron_network)
        case _:
            db_url = f"postgresql://{os.getenv('POSTGRES_USER')}:" \
                     f"{os.getenv('POSTGRES_PASSWORD')}@" \
                     f"{os.getenv('POSTGRES_HOST', 'localhost')}:" \
                     f"{os.getenv('POSTGRES_PORT')}/" \
                     f"{os.getenv('POSTGRES_DB')}"
            config = Config(db_url=db_url)
    return config
