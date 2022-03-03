import logging.config
import json

from fastapi import APIRouter, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from chat_core.chat_domain import ChatApiRequest, ChatApiResponse, UserRequest
from layer_model.domain import SimpleRequest, BotResponse
from utility.api_endpoint import get_chat_api_response, get_mecab_ner_response

from config.settings import config_basic
from utility.custom_error import DockerNetworkException

logging.config.dictConfig(config_basic)
logger = logging.getLogger('simple_log')


router = APIRouter(
    prefix="/chat_middleware",
    tags=["chat_middleware"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_middleware")
async def request_from_django_web(django_req: SimpleRequest, request: Request) -> BotResponse:

    try:

        user_request = UserRequest(user_sentence=django_req.user_sentence, user_ip=request.client.host, user_request_time=django_req.user_request_time)

        mecab_ner_response = get_mecab_ner_response(user_request.json())

        logger.info({'status': 'success', 'user_ip': request.client.host, "request_path": request.url.path,
                     "return": mecab_ner_response})

        chat_api_response = get_chat_api_response(json.dumps(mecab_ner_response, default=str))

        logger.info({'status': 'success', 'user_ip': request.client.host, "request_path": request.url.path,
                     "return": chat_api_response})

        c_m_res = BotResponse(bot_response=chat_api_response)

    except ValidationError as e:
        raise Exception

    return jsonable_encoder(c_m_res)


@router.post("/test_mecab_ner")
async def request_mecab_ner(django_req: Request):
    try:
        mecab_ner_response = get_mecab_ner_response(django_req.json())
        return jsonable_encoder(mecab_ner_response)

    except ValidationError as e:
        return e.json()


@router.post("/test_chat_api")
async def request_chat_api(chat_api_req: ChatApiRequest, request: Request) -> BotResponse:

    try:

        chat_api_response = get_chat_api_response(chat_api_req.json())

        c_a_res = ChatApiResponse(api_response=chat_api_response, api_server="chat_api_template")

        logger.info({'status': 'success', 'user_ip': request.client.host, "request_path": request.url.path,
                     "return": c_a_res})

        c_m_res = BotResponse(bot_response=chat_api_response)

        return jsonable_encoder(c_m_res)

    except DockerNetworkException as dne:
        logger.error({'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": dne})
        raise HTTPException(status_code=418, detail=dne)
    except Exception as e:
        logger.critical({'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": e})
        raise
