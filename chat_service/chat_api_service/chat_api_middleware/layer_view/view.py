import logging.config

from fastapi import APIRouter, Request
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from layer_control.control import get_template_data
from chat_core.chat_domain import ChatApiRequest, ChatApiResponse, TemplateRequestData
from utility.api_endpoint import get_youtube_api_response, get_mrc_api_response

from config.settings import config_basic
from utility.custom_error import TemplateNotExist

logging.config.dictConfig(config_basic)
logger = logging.getLogger('simple_log')


BLANK_LIST = 0
FIRST_VALUE = 0

router = APIRouter(
    prefix="/chat_api",
    tags=["chat_api"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_api")
async def request_from_chat_middleware(chat_api_req: ChatApiRequest, request: Request):
    try:

        if len(chat_api_req.sentence_attributes) == BLANK_LIST:
            c_a_res = ChatApiResponse(api_response="잘 모르겠어요. 알려주세요!", api_server="empty_template")
            logger.info({'status': 'success', 'user_ip': request.client.host, "request_path": request.url.path,
                         "return": c_a_res})
            return jsonable_encoder(c_a_res)

        middle_m_n_a = chat_api_req.sentence_attributes[FIRST_VALUE]
        t_r_d = TemplateRequestData(main_category=middle_m_n_a.main_category, entity_medium_category=middle_m_n_a.entity_medium_category,
                           entity=middle_m_n_a.entity, intent_small_category=middle_m_n_a.intent_small_category)

        if middle_m_n_a.main_category == "music":
            youtube_response = get_youtube_api_response(chat_api_req.json())
            c_a_res = ChatApiResponse(api_response=youtube_response, api_server="youtube_template")
            logger.info({'status': 'success', 'user_ip': request.client.host, "request_path": request.url.path,
                         "return": c_a_res})
            return jsonable_encoder(c_a_res)

        if middle_m_n_a.main_category == "question":
            mrc_response = get_mrc_api_response(chat_api_req.json())
            c_a_res = ChatApiResponse(api_response="MRC 응답입니다.", api_server="mrc_template")
            logger.info({'status': 'success', 'user_ip': request.client.host, "request_path": request.url.path,
                         "return": c_a_res})
            return jsonable_encoder(c_a_res)

        api_template = get_template_data(t_r_d)
        if api_template:
            c_a_res = ChatApiResponse(api_response=api_template, api_server="basic_template")
            logger.info({'status': 'success', 'user_ip': request.client.host, "request_path": request.url.path,
                         "return": c_a_res})
            return jsonable_encoder(c_a_res)

    except ValidationError as ve:
        logger.error(
            {'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": ve})
        return ve.json()

    except TemplateNotExist as fne:
        logger.error(
            {'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": fne})
        raise TemplateNotExist(fne)

    except Exception as e:
        logger.critical({'status': 'fail', 'user_ip': request.client.host, "request_path": request.url.path, "message": e})
        return jsonable_encoder(e)
    return jsonable_encoder(False)

