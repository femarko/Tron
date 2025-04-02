from src.orm_tool.sql_aclchemy_wrapper import orm_conf
from src.config import load_config

config = load_config()


orm_conf.start_mapping()
orm_conf.drop_tables()
orm_conf.create_tables()