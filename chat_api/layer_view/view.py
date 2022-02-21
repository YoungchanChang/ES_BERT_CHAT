from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from chat_api.layer_control.control import get_template_data
from chat_api.layer_model.domain import ChatApiRequest, ChatApiResponse, TemplateRequestData
from chat_middleware.layer_model.domain import ChatMiddlewareResponse, Request

router = APIRouter(
    prefix="/chat_api",
    tags=["chat_api"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_api")
async def request_from_chat_middleware(chat_api_req: ChatApiRequest):
    try:
        middle_m_n_a = chat_api_req.m_n_a
        t_r_d = TemplateRequestData(main_category=middle_m_n_a.main_category, entity_medium_category=middle_m_n_a.entity_medium_category,
                           entity=middle_m_n_a.entity, intent_small_category=middle_m_n_a.intent_small_category)
        api_template = get_template_data(t_r_d)
        if api_template:
            c_a_res = ChatApiResponse(api_response=api_template, api_server="basic_template", system_response_time="2022-02-21T07:03:52.716025")
            return jsonable_encoder(c_a_res)
    except ValidationError as e:
        return e.json()
    return jsonable_encoder(False)

