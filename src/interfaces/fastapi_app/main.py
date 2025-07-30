from fastapi import FastAPI, Depends

from src.infrastructure.orm.sql_aclchemy_wrapper import orm_conf
from src.interfaces.fastapi_app.urls import tron_router


app = FastAPI(dependencies=[Depends(orm_conf.start_mapping)])
app.include_router(tron_router)
