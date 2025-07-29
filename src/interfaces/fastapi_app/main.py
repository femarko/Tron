import uvicorn
from fastapi import FastAPI, Depends

from src.infrastructure.orm.sql_aclchemy_wrapper import orm_conf
from src.config import settings
from src.interfaces.fastapi_app.urls import tron_router


app = FastAPI(dependencies=[Depends(orm_conf.start_mapping)])
app.include_router(tron_router)


def run_app():
    # if settings.mode in {"test", "dev"}:
    #     uvicorn.run(app=app, host="127.0.0.1", port=800
    # else:
    #     uvicorn.run(app=app, host="0.0.0.0", port=8000)
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)


if __name__ == "__main__":
    run_app()
    print()