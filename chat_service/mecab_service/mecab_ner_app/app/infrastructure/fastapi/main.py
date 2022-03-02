import uvicorn
from fastapi import FastAPI, APIRouter
from app.domain.entity import Query, CategoryItem, MecabWord
from app.infrastructure.fastapi import mecab_api, data_api
from app.utility.docker_net import get_entity_intent_answer
from app.controller.service.mecab_controller import get_data, MecabDataController
from fastapi.encoders import jsonable_encoder

app = FastAPI()

app.include_router(mecab_api.router)
app.include_router(data_api.router)


if __name__ == "__main__":
    uvicorn.run(
        "app.infrastructure.fastapi.main:app", host="0.0.0.0", port=5100, reload=True
    )