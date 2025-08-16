from src.bootstrap.bootstrap import container


if __name__ == "__main__":
    container.orm_conf.start_mapping()
    container.orm_conf.drop_tables()
    container.orm_conf.create_tables()