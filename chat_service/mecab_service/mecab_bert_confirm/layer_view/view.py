from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from chat_core.chat_domain import ChatApiRequest

router = APIRouter(
    prefix="/mecab_bert",
    tags=["mecab_bert"],
    responses={404: {"description": "Not found"}},
)


@router.post("/bert_confirm")
async def get_bert_confirm(c_a_req: ChatApiRequest):

    for x_bert_item in c_a_req.mecab_bert_bind:
        x_bert_item.bert_confirm = True

    for x_bert_item in c_a_req.entities:
        x_bert_item.bert_confirm = True

    for x_bert_item in c_a_req.intents:
        x_bert_item.bert_confirm = True

    return jsonable_encoder(c_a_req)
