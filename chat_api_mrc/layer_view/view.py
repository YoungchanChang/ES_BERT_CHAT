from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import ValidationError

from chat_api_mrc.layer_control.control import get_mrc
from chat_api_mrc.layer_model.domain import ChatApiRequest, ChatApiResponse

router = APIRouter(
    prefix="/chat_api_mrc",
    tags=["chat_api_mrc"],
    responses={404: {"description": "Not found"}},
)


@router.post("/response_mrc")
async def request_from_chat_api(chat_api_req: ChatApiRequest):

    try:
        mrc_res = get_mrc(chat_api_req.sentence_attributes)
        c_a_res = ChatApiResponse(api_response=mrc_res, api_server="youtube_template")
        return jsonable_encoder(c_a_res)

    except ValidationError as e:
        return e.json()
