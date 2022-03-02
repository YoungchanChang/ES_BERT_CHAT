import uvicorn
from fastapi import FastAPI
from app.infrastructure.fastapi import mecab_api, data_api

app = FastAPI()

app.include_router(mecab_api.router)
# app.include_router(data_api.router)


if __name__ == "__main__":
    uvicorn.run(
        "app.infrastructure.fastapi.main:app", host="0.0.0.0", port=5100, reload=True
    )