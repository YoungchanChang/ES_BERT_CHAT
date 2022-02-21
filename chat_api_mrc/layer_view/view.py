from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from chat_middleware.layer_model.domain import ChatMiddlewareResponse, Request

router = APIRouter(
    prefix="/chat_api_mrc",
    tags=["chat_api_mrc"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_mrc")
async def request_from_chat_api(django_req: Request):
    try:
        c_m_res = ChatMiddlewareResponse(bot_response="Hello")
    except ValidationError as e:
        return e.json()

    return jsonable_encoder(c_m_res)
