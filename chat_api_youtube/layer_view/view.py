from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from chat_api_youtube.layer_model.domain import ChatApiRequest, ChatApiResponse

router = APIRouter(
    prefix="/chat_api_youtube",
    tags=["chat_api_youtube"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_youtube")
async def request_from_chat_api(chat_api_req: ChatApiRequest):
    try:
        c_a_res = ChatApiResponse(api_template="나도 치킨이 좋아요", api_server="basic_template", system_response_time="2022-02-21T07:03:52.716025")
    except ValidationError as e:
        return e.json()

    return jsonable_encoder(c_a_res)
