from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from chat_middleware.layer_model.domain import ChatMiddlewareResponse, Request

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
