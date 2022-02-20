from pathlib import Path
from scripts.db_info import *
from app.application.service.mecab_generator import MecabGenerator

ENTITY_DIR_PATH = Path(__file__).resolve().parent.parent.joinpath("datas", 'entities', 'storage')
print(ENTITY_DIR_PATH)
m_g = MecabGenerator(storage_path=str(ENTITY_DIR_PATH))
# for path_item in Path(m_g.mecab_path).iterdir():
#     print(path_item)

# init data
m_g = MecabGenerator(storage_path=str(ENTITY_DIR_PATH))

MecabEntity.drop_table()
EntityCategoryItem.drop_table()
EntityCategoryItem.create_table()
MecabEntity.create_table()


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
