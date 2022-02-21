from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from chat_middleware.layer_model.domain import ChatMiddlewareResponse, Request, ChatApiRequest, ChatApiResponse
from chat_middleware.utility.api_endpoint import get_chat_api_response

router = APIRouter(
    prefix="/chat_middleware",
    tags=["chat_middleware"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_middleware")
async def request_from_django_web(django_req: Request):
    try:
        c_m_res = ChatMiddlewareResponse(bot_response="Hello")
    except ValidationError as e:
        return e.json()

    return jsonable_encoder(c_m_res)


@router.post("/test_chat_api")
async def request_chat_api(chat_api_req: ChatApiRequest):
    try:
        chat_api_response = get_chat_api_response(chat_api_req.json())
        c_a_res = ChatApiResponse(api_response=chat_api_response, api_server="chat_api_template")
        return jsonable_encoder(c_a_res)

    except ValidationError as e:
        return e.json()
