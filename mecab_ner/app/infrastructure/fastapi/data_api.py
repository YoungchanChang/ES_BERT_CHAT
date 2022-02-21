from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from app.controller.service.mecab_controller import MecabDataController
from app.domain.entity import CategoryItem, MecabWord

router = APIRouter(
    prefix="/mecab_data",
    tags=["mecab_data"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create_index")
async def create_index(category_item: CategoryItem):
    is_index_created = MecabDataController.create_index(category_item)
    return_json = {"result": is_index_created}
    return jsonable_encoder(return_json)


@router.post("/insert_data")
async def insert_data(mecab_word: MecabWord):
    is_index_created = MecabDataController.insert_data(mecab_word)
    return_json = {"result": is_index_created}
    return jsonable_encoder(return_json)