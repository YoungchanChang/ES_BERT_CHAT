import os

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.application.service.mecab_parser import MeCabParser
from app.controller.service.mecab_controller import get_data
from app.domain.endpoint import ChatApiRequest, Request
from app.domain.entity import Query
from app.infrastructure.network.api_endpoint import get_bert_confirm_response

router = APIRouter(
    prefix="/mecab_ner",
    tags=["mecab_ner"],
    responses={404: {"description": "Not found"}},
)


@router.post("/mecab_attribute")
async def get_mecab_attribute(req: Request):
    sentence_attributes = jsonable_encoder(get_data(sentence=req.user_sentence))
    return_json = {"req": req, "sentence_attributes": sentence_attributes}

    return jsonable_encoder(return_json)


@router.post("/mecab_analyzed")
async def get_mecab_analyzed(req: Query):
    mecab_parsed_list = list(MeCabParser(sentence=req.sentence).gen_mecab_compound_token_feature())
    return_json = {"result": mecab_parsed_list}

    return jsonable_encoder(return_json)
