import uvicorn
from fastapi import FastAPI

from dotenv import load_dotenv

from app.domain.entity import Query, CategoryItem, MecabWord
from app.utility.docker_net import get_entity_intent_answer

load_dotenv()
from app.controller.service.mecab_controller import get_data, MecabDataController

app = FastAPI()

from fastapi.encoders import jsonable_encoder


@app.post("/mecab_entity")
async def create_item(sentence: Query):
    return_json = {"answer": jsonable_encoder(get_data(sentence=sentence.sentence))}
    return jsonable_encoder(return_json)


@app.post("/mecab_entity/bert_chat")
async def bert_chat(sentence: Query):
    return_json = {"answer": jsonable_encoder(get_data(sentence=sentence.sentence))}
    return_val = get_entity_intent_answer(return_json)
    return_json = {"answer": return_val}
    return jsonable_encoder(return_json)


@app.post("/mecab_entity/create_index")
async def create_index(category_item: CategoryItem):
    is_index_created = MecabDataController.create_index(category_item)
    return_json = {"answer": is_index_created}
    return jsonable_encoder(return_json)


@app.post("/mecab_entity/insert_data")
async def insert_data(mecab_word: MecabWord):
    is_index_created = MecabDataController.insert_data(mecab_word)
    return_json = {"answer": is_index_created}
    return jsonable_encoder(return_json)



if __name__ == "__main__":
    uvicorn.run(
        "app.infrastructure.fastapi.main:app", host="0.0.0.0", port=7000, reload=True
    )