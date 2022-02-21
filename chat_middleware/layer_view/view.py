import json

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from chat_middleware.layer_model.domain import ChatMiddlewareResponse, Request, ChatApiRequest, ChatApiResponse
from chat_middleware.utility.api_endpoint import get_chat_api_response, get_mecab_ner_response

router = APIRouter(
    prefix="/chat_middleware",
    tags=["chat_middleware"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_middleware")
async def request_from_django_web(django_req: Request):
    try:
        mecab_ner_response = get_mecab_ner_response(django_req.json())

        chat_api_response = get_chat_api_response(json.dumps(mecab_ner_response, default=str))
        c_m_res = ChatMiddlewareResponse(bot_response=chat_api_response)
    except ValidationError as e:
        return e.json()

    return jsonable_encoder(c_m_res)


@router.post("/test_mecab_ner")
async def request_mecab_ner(django_req: Request):
    try:
        mecab_ner_response = get_mecab_ner_response(django_req.json())
        return jsonable_encoder(mecab_ner_response)

    except ValidationError as e:
        return e.json()


@router.post("/test_chat_api")
async def request_chat_api(chat_api_req: ChatApiRequest):
    try:
        chat_api_response = get_chat_api_response(chat_api_req.json())
        c_a_res = ChatApiResponse(api_response=chat_api_response, api_server="chat_api_template")
        return jsonable_encoder(c_a_res)

    except ValidationError as e:
        return e.json()
