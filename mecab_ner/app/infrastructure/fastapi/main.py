import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

from mecab_ner.app.controller.service.mecab_controller import get_data

class Query(BaseModel):
    sentence: str

app = FastAPI()

from fastapi.encoders import jsonable_encoder
@app.post("/mecab_entity")
async def create_item(sentence: Query):
    return jsonable_encoder(get_data(sentence=sentence.sentence))


if __name__ == "__main__":
    uvicorn.run(
        "mecab_ner.app.infrastructure.fastapi.main:app", host="0.0.0.0", port=8000, reload=True
    )