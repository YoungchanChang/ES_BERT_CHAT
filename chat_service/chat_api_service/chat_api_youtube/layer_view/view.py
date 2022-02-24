import logging.config

from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from layer_control.control import get_youtube_music
from utility.custom_error import NoMusicData
from chat_core.chat_domain import ChatApiRequest, ChatApiResponse


from config.settings import config_basic

logging.config.dictConfig(config_basic)
logger = logging.getLogger('simple_log')

router = APIRouter(
    prefix="/chat_api_youtube",
    tags=["chat_api_youtube"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_youtube")
async def request_from_chat_api(chat_api_req: ChatApiRequest, request: Request):

    try:
        youtube_res = get_youtube_music(chat_api_req.sentence_attributes)
        c_a_res = ChatApiResponse(api_response=youtube_res, api_server="youtube_template")
        logger.info({'status': 'success', 'user_ip': request.client.host, "request_path": request.url.path, "return": c_a_res})
        return jsonable_encoder(c_a_res)

    except ValidationError as ve:
        logger.error(
            {'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": ve})
        return ve.json()
    except NoMusicData as me:
        logger.warning(
            {'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": me,
             "music_request": chat_api_req.sentence_attributes})
    except Exception as e:
        logger.critical(
            {'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": e})
    c_a_res = ChatApiResponse(api_response="음악을 준비중이예요. 조금만 기다려주세요.", api_server="basic_template")
    return jsonable_encoder(c_a_res)

