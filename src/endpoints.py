from orm_tool.sql_aclchemy_wrapper import orm_conf
from service_layer import app_manager, unit_of_work


orm_conf.start_mapping()
orm_conf.create_tables()

