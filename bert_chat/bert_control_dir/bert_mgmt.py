from bert_db_dir.bert_txt import read_txt
from utility_dir import utility_string
ENTITY_SMALL_CATEGORY = 0
INTENT_SMALL_CATEGORY = 1
TEMPLATE_IDX = 2


def get_template_data(entity_large_category, entity_medium_category, entity, intent_small_category):

    """엔티티 대분류, 중분류에 따라 인텐트 템플릿에 넣고 반환하는함수"""

    for data_item in read_txt(entity_large_category):
        if data_item[ENTITY_SMALL_CATEGORY] == entity_medium_category and data_item[INTENT_SMALL_CATEGORY] == intent_small_category:
            josa_sbj = utility_string.get_marker(entity, "josa_sbj")
            josa_obj = utility_string.get_marker(entity, "josa_obj")
            hint = data_item[TEMPLATE_IDX].replace("{entity}", entity)
            hint = hint.replace("{josa_sbj}", josa_sbj)
            hint = hint.replace("{josa_obj}", josa_obj)
            return hint
    return False
