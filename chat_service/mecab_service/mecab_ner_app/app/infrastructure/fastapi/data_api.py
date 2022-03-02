from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.application.service.django_data import DjangoDataController
from app.domain.data_domain import CategoryIndex, MecabWord

router = APIRouter(
    prefix="/mecab_data",
    tags=["mecab_data"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create_index")
async def create_index(category_index: CategoryIndex):
    is_index_created = DjangoDataController.create_index(category_index)
    return_json = {"result": is_index_created}
    return jsonable_encoder(return_json)


@router.post("/insert_data")
async def insert_data(mecab_word: MecabWord):
    is_index_created = DjangoDataController.insert_data(mecab_word)
    return_json = {"result": is_index_created}
    return jsonable_encoder(return_json)