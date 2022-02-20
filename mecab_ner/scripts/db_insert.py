from pathlib import Path
from scripts.db_info import *
from app.application.service.mecab_generator import MecabGenerator

def set_entity_table():
    MecabEntity.drop_table()
    EntityCategoryItem.drop_table()
    EntityCategoryItem.create_table()
    MecabEntity.create_table()

def insert_entity_data():
    ENTITY_DIR_PATH = Path(__file__).resolve().parent.parent.joinpath("datas", 'entities', 'storage')
    m_g = MecabGenerator(storage_path=str(ENTITY_DIR_PATH))
    for data_item in m_g.gen_all_mecab_category_data(m_g.storage_path, need_parser=True):
        large_category, medium_category, data_dict = data_item
        for data_dict_item in data_dict.keys():
            small_category = data_dict_item.replace("#", "").strip()
            EntityCategoryItem.create(large_category=large_category,
                                      medium_category=medium_category,
                                      small_category=small_category)


    for data_item in m_g.gen_all_mecab_category_data(m_g.storage_path, need_parser=True):
        large_category, medium_category, data_dict = data_item
        for data_dict_item in data_dict.keys():
            small_category = data_dict_item.replace("#", "").strip()
            entity_val = EntityCategoryItem.get_or_none(EntityCategoryItem.large_category == large_category,
                                   EntityCategoryItem.medium_category == medium_category,
                                   EntityCategoryItem.small_category == small_category)

            for data_dict_val in data_dict[data_dict_item]:
                word, mecab_word = data_dict_val
                MecabEntity.create(word=word, mecab_word=mecab_word, category=entity_val.id)


def set_intent_table():
    MecabIntent.drop_table()
    IntentCategoryItem.drop_table()
    IntentCategoryItem.create_table()
    MecabIntent.create_table()


def insert_intent_data():
    INTENT_DIR_PATH = Path(__file__).resolve().parent.parent.joinpath("datas", 'intents', 'storage')
    m_g = MecabGenerator(storage_path=str(INTENT_DIR_PATH))
    for data_item in m_g.gen_all_mecab_category_data(m_g.storage_path, need_parser=True):
        large_category, medium_category, data_dict = data_item
        for data_dict_item in data_dict.keys():
            small_category = data_dict_item.replace("#", "").strip()
            IntentCategoryItem.create(large_category=large_category,
                                      medium_category=medium_category,
                                      small_category=small_category)


    for data_item in m_g.gen_all_mecab_category_data(m_g.storage_path, need_parser=True):
        large_category, medium_category, data_dict = data_item
        for data_dict_item in data_dict.keys():
            small_category = data_dict_item.replace("#", "").strip()
            entity_val = IntentCategoryItem.get_or_none(IntentCategoryItem.large_category == large_category,
                                   IntentCategoryItem.medium_category == medium_category,
                                   IntentCategoryItem.small_category == small_category)

            for data_dict_val in data_dict[data_dict_item]:
                word, mecab_word = data_dict_val
                MecabIntent.create(word=word, mecab_word=mecab_word, category=entity_val.id)

if __name__ == "__main__":
    set_intent_table()
    insert_intent_data()