import logging.config

from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError


from layer_control.control import get_mrc
from chat_core.chat_domain import ChatApiRequest, ChatApiResponse

from config.settings import config_basic

logging.config.dictConfig(config_basic)
logger = logging.getLogger('simple_log')

router = APIRouter(
    prefix="/chat_api_mrc",
    tags=["chat_api_mrc"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_mrc")
async def request_from_chat_api(chat_api_req: ChatApiRequest, request: Request):
    try:

        mrc_res = get_mrc(chat_api_req.mecab_bert_bind[0].bind_sentence)
        c_a_res = ChatApiResponse(api_response=mrc_res, api_server="mrc_template")

        logger.info({'status': 'success', 'user_ip': request.client.host, "request_path": request.url.path, "return": c_a_res})
        return jsonable_encoder(c_a_res)

    except ValidationError as ve:
        logger.error({'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": ve})
        return ve.json()

    except Exception as e:
        logger.critical({'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": e})
        return jsonable_encoder(e)
