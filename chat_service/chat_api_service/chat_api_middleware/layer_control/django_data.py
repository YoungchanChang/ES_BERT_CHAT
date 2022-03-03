from pathlib import Path
from typing import List

from peewee import DoesNotExist

from layer_model.fastapi_domain import TemplateItemRequest, TemplateCategoryRequest
from layer_model.mysql_domain import EntityIntentCategoryTemplate, EntityIntentItemTemplate, MecabEntityItem, \
    MecabIntentItem


def write_txt(path: str, txt_item: str):
    """텍스트 파일 쓰는 메소드"""

    with open(path, "a", encoding='UTF8') as file:
        data = "\n" + str(txt_item)
        file.write(data)


class DjangoDataController:
    BASE_DIR_PATH = Path(__file__).resolve().parent.parent.joinpath("datas")


    @classmethod
    def insert_template_item(cls, temp_item_req: TemplateItemRequest):

        category_name = "template_item.txt"

        item_path = cls.BASE_DIR_PATH.joinpath(category_name)
        try:
            entity_item_val = MecabEntityItem.get_by_id(temp_item_req.entity_item_id)
            intent_item_val = MecabIntentItem.get_or_none(temp_item_req.intent_item_id)
            save_str = entity_item_val.word + "," + intent_item_val.word + "," + temp_item_req.template

            en_cat_temp = EntityIntentItemTemplate.get_or_create(entity_item=temp_item_req.entity_item_id,
                                                       intent_item=temp_item_req.intent_item_id,
                                                       template=temp_item_req.template)

            if en_cat_temp[1]:
                write_txt(str(item_path), save_str)
                return True
        except DoesNotExist as dne:
            print(dne)
            return False
        return False
#


    @classmethod
    def insert_template_category(cls, temp_cat_req: TemplateCategoryRequest):
        try:
            category_name = "template_" + temp_cat_req.bind_category + ".txt"
            item_path = cls.BASE_DIR_PATH.joinpath("chat_templates", category_name)

            save_str = temp_cat_req.entity_category + "," + temp_cat_req.intent_category + "," + temp_cat_req.template
            e_i_cat_tmp = EntityIntentCategoryTemplate.get_or_create(bind_category=temp_cat_req.bind_category,
                                                            entity_category=temp_cat_req.entity_category,
                                                           intent_category=temp_cat_req.intent_category,
                                                           template=temp_cat_req.template)
            if e_i_cat_tmp[1]:
                write_txt(str(item_path), save_str)
                return True
        except Exception as e:
            print(e)
        return False