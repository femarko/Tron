from src.infrastructure.orm.sql_aclchemy_wrapper import orm_conf


orm_conf.start_mapping()
orm_conf.drop_tables()
orm_conf.create_tables()