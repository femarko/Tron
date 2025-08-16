from fastapi import FastAPI, Depends
from src.interfaces.fastapi_app.urls import tron_router

from src.bootstrap.bootstrap import container


app = FastAPI(dependencies=[Depends(container.orm_conf.start_mapping)])
app.include_router(tron_router)
