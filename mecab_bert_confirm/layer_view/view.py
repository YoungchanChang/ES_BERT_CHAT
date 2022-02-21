from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder

from mecab_bert_confirm.layer_model.domain import BertConfirmResponse, MecabNerAttribute

router = APIRouter(
    prefix="/mecab_bert",
    tags=["mecab_bert"],
    responses={404: {"description": "Not found"}},
)


@router.post("/bert_confirm")
async def get_bert_confirm(m_n_attr: MecabNerAttribute):
    b_c_res = BertConfirmResponse(bert_confirm=True)
    return jsonable_encoder(b_c_res)
