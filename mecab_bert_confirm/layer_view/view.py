from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from mecab_bert_confirm.layer_model.domain import MecabNerRequest, MecabNerResponse

router = APIRouter(
    prefix="/mecab_bert",
    tags=["mecab_bert"],
    responses={404: {"description": "Not found"}},
)


@router.post("/bert_confirm")
async def create_item(m_n_req: MecabNerRequest):
    print(m_n_req)
    m_n_res = MecabNerResponse(bert_confirm=True)
    return jsonable_encoder(m_n_res)
