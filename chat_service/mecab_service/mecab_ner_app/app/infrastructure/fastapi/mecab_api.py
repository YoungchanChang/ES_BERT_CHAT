import os

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.application.service.mecab_parser import MecabParser
from app.controller.service.bert_sender import get_mecab_bind_feature
from app.infrastructure.network.api_endpoint import get_bert_confirm_response
from chat_service.chat_core.chat_domain import UserRequest, ChatApiRequest

router = APIRouter(
    prefix="/mecab_ner",
    tags=["mecab_ner"],
    responses={404: {"description": "Not found"}},
)


@router.post("/mecab_attribute")
async def get_mecab_attribute(req: UserRequest):
    m_b_d_list, entity_list, intent_list = get_mecab_bind_feature(sentence=req.user_sentence)
    bert_request = ChatApiRequest(user_info=req, mecab_bert_bind=m_b_d_list,
                                  entities=entity_list,
                                  intents=intent_list)
    youtube_response = get_bert_confirm_response(bert_request.json())

    return jsonable_encoder(youtube_response)


@router.post("/mecab_analyzed")
async def get_mecab_analyzed(req: UserRequest):
    mecab_parsed_list = list(MecabParser(sentence=req.user_sentence).gen_mecab_compound_token_feature())
    return_json = {"result": mecab_parsed_list}

    return jsonable_encoder(return_json)
