from pathlib import Path
from scripts.db_info import *
from app.application.service.mecab_generator import MecabGenerator

ENTITY_DIR_PATH = Path(__file__).resolve().parent.parent.joinpath("datas", 'entities', 'storage')
print(ENTITY_DIR_PATH)
m_g = MecabGenerator(storage_path=str(ENTITY_DIR_PATH))
for path_item in Path(m_g.mecab_path).iterdir():
    print(path_item)

# init data
m_g = MecabGenerator(storage_path=ENTITY_DIR_PATH)

EntityCategoryItem.drop_table()
EntityCategoryItem.create_table()
for data_item in m_g.gen_all_mecab_category_data(m_g.storage_path, need_parser=True):
    large_category, medium_category, data_dict = data_item
    for data_dict_item in data_dict.keys():
        # large_category
        # medium_category
        # small_category
        small_category = data_dict_item.replace("#", "").strip()
        EntityCategoryItem.create(large_category=large_category,
                                  medium_category=medium_category,
                                  small_category=small_category)
        print(data_dict_item)
    print(large_category)
    print(medium_category)
    print(data_dict)

