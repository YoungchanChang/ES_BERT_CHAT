from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from chat_api.layer_control.control import get_template_data
from chat_api.layer_model.domain import ChatApiRequest, ChatApiResponse, TemplateRequestData
from chat_api.utility.api_endpoint import get_youtube_api_response, get_mrc_api_response

BLANK_LIST = 0
FIRST_VALUE = 0

router = APIRouter(
    prefix="/chat_api",
    tags=["chat_api"],
    responses={404: {"description": "Not found"}},
)

@router.post("/response_api")
async def request_from_chat_middleware(chat_api_req: ChatApiRequest):
    try:

        if len(chat_api_req.sentence_attributes) == BLANK_LIST:
            c_a_res = ChatApiResponse(api_response="잘 모르겠어요. 알려주세요!", api_server="empty_template")
            return jsonable_encoder(c_a_res)

        middle_m_n_a = chat_api_req.sentence_attributes[FIRST_VALUE]
        t_r_d = TemplateRequestData(main_category=middle_m_n_a.main_category, entity_medium_category=middle_m_n_a.entity_medium_category,
                           entity=middle_m_n_a.entity, intent_small_category=middle_m_n_a.intent_small_category)

        if middle_m_n_a.main_category == "music":
            youtube_response = get_youtube_api_response(chat_api_req.json())
            c_a_res = ChatApiResponse(api_response=youtube_response, api_server="youtube_template")
            return jsonable_encoder(c_a_res)

        if middle_m_n_a.main_category == "question":
            mrc_response = get_mrc_api_response(chat_api_req.json())
            c_a_res = ChatApiResponse(api_response="MRC 응답입니다.", api_server="mrc_template")
            return jsonable_encoder(c_a_res)

        api_template = get_template_data(t_r_d)
        if api_template:
            c_a_res = ChatApiResponse(api_response=api_template, api_server="basic_template")
            return jsonable_encoder(c_a_res)
    except ValidationError as e:
        return e.json()
    except Exception as e:
        print(e)
        return jsonable_encoder(False)
    return jsonable_encoder(False)

