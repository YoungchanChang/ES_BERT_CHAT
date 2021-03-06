from pathlib import Path

from app.application.service.mecab_reader import MecabDataController
from app.domain.data_domain import EntityCategoryItem, MecabEntityItem, MecabIntentItem, IntentCategoryItem, \
    EntityIntentItemTemplate, EntityIntentCategoryTemplate
from domain.mecab_exception import MecabDataReaderException


def set_entity_table():
    MecabEntityItem.drop_table()
    EntityCategoryItem.drop_table()
    EntityCategoryItem.create_table()
    MecabEntityItem.create_table()


class MecabEntityModel(MecabDataController):
    def _set_mecab_path(self, ner_path: str) -> None:
        self.mecab_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "entities",
                                                                                        "mecab_data")

        if self._clear_mecab_dir:
            self._clear_dir()

class MecabIntentInsert(MecabDataController):
    def _set_mecab_path(self, ner_path: str) -> None:
        self.mecab_path = Path(__file__).resolve().parent.parent.parent.parent.joinpath("data", "entities",
                                                                                        "mecab_data")

        if self._clear_mecab_dir:
            self._clear_dir()


def insert_entity_data():
    """
    엔티티 데이터 삽입
    - 카테고리 먼저 생성
    - 데이터 삽입
    """
    ENTITY_DIR_PATH = Path(__file__).resolve().parent.parent.joinpath("data", 'entities', 'entity_data')
    m_g = MecabEntityModel(ner_path=str(ENTITY_DIR_PATH))
    for data_item in m_g.gen_all_mecab_category_data(m_g.ner_path, use_mecab_parser=True):
        large_category, data_dict = data_item
        medium_category = large_category
        if "_" in large_category:
            category_general = large_category.split("_")
            large_category = category_general[0]
            medium_category = category_general[1]

        for data_dict_item in data_dict.keys():
            small_category = data_dict_item.replace("#", "").strip()
            EntityCategoryItem.create(large_category=large_category,
                                      medium_category=medium_category,
                                      small_category=small_category)


    for data_item in m_g.gen_all_mecab_category_data(m_g.ner_path, use_mecab_parser=True):
        large_category, data_dict = data_item
        medium_category = large_category
        if "_" in large_category:
            category_general = large_category.split("_")
            large_category = category_general[0]
            medium_category = category_general[1]

        for data_dict_item in data_dict.keys():
            small_category = data_dict_item.replace("#", "").strip()
            entity_val = EntityCategoryItem.get_or_none(EntityCategoryItem.large_category == large_category,
                                   EntityCategoryItem.medium_category == medium_category,
                                   EntityCategoryItem.small_category == small_category)

            for data_dict_val in data_dict[data_dict_item]:
                word, mecab_word = data_dict_val
                MecabEntityItem.create(word=word, mecab_word=mecab_word, category=entity_val.id)


def set_intent_table():
    MecabIntentItem.drop_table()
    IntentCategoryItem.drop_table()
    IntentCategoryItem.create_table()
    MecabIntentItem.create_table()


def insert_intent_data():
    ENTITY_DIR_PATH = Path(__file__).resolve().parent.parent.joinpath("data", 'intents', 'intent_data')
    m_g = MecabIntentInsert(ner_path=str(ENTITY_DIR_PATH))
    for data_item in m_g.gen_all_mecab_category_data(m_g.ner_path, use_mecab_parser=True):
        large_category, data_dict = data_item
        medium_category = large_category
        if "_" in large_category:
            category_general = large_category.split("_")
            large_category = category_general[0]
            medium_category = category_general[1]

        for data_dict_item in data_dict.keys():
            small_category = data_dict_item.replace("#", "").strip()
            IntentCategoryItem.create(large_category=large_category,
                                      medium_category=medium_category,
                                      small_category=small_category)


    for data_item in m_g.gen_all_mecab_category_data(m_g.ner_path, use_mecab_parser=True):

        large_category, data_dict = data_item
        medium_category = large_category
        if "_" in large_category:
            category_general = large_category.split("_")
            large_category = category_general[0]
            medium_category = category_general[1]

        for data_dict_item in data_dict.keys():
            small_category = data_dict_item.replace("#", "").strip()
            entity_val = IntentCategoryItem.get_or_none(IntentCategoryItem.large_category == large_category,
                                   IntentCategoryItem.medium_category == medium_category,
                                   IntentCategoryItem.small_category == small_category)

            for data_dict_val in data_dict[data_dict_item]:
                word, mecab_word = data_dict_val
                MecabIntentItem.create(word=word, mecab_word=mecab_word, category=entity_val.id)


def read_txt(path):
    """텍스트 파일 읽는 메소드"""
    with open(path, "r", encoding='utf-8-sig') as file:
        txt_list = file.read().splitlines()
        text_template = [x for x in txt_list if len(x.split(",")) == 3]
        return text_template

def insert_template_item_data():
    TEMPLATE_BASIC_PATH = Path(__file__).resolve().parent.parent.parent.parent.joinpath("chat_api_service", 'chat_api_middleware', 'datas')
    ENTITY_DIR_PATH = TEMPLATE_BASIC_PATH.joinpath("chat_templates")

    template_item = TEMPLATE_BASIC_PATH.joinpath("template_item.txt")

    for text_item in read_txt(str(template_item)):
        entity_item, intent_item, template_sentence = text_item.split(",")

        entity_item_val = MecabEntityItem.get_or_none(MecabEntityItem.word == entity_item)
        intent_item_val = MecabIntentItem.get_or_none(MecabIntentItem.word == intent_item)

        if (entity_item_val is not None) and (intent_item_val is not None):
            EntityIntentItemTemplate.get_or_create(entity_item=entity_item_val, intent_item=intent_item_val, template=template_sentence)

    for path_item in ENTITY_DIR_PATH.iterdir():
        split_template_path = path_item.stem.split("_")
        large_category = split_template_path[0]
        bind_category = split_template_path[1]
        for text_item in read_txt(str(path_item)):
            entity_category, intent_category, template_sentence = text_item.split(",")
            EntityIntentCategoryTemplate.get_or_create(bind_category=bind_category, entity_category=entity_category,
                                            intent_category=intent_category,
                                            template=template_sentence)

if __name__ == "__main__":

    EntityIntentItemTemplate.drop_table()
    EntityIntentCategoryTemplate.drop_table()

    set_entity_table()
    insert_entity_data()

    set_intent_table()
    insert_intent_data()

    EntityIntentItemTemplate.create_table()
    EntityIntentCategoryTemplate.create_table()
    insert_template_item_data()