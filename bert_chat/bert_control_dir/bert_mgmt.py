from bert_db_dir.bert_txt import read_txt

ENTITY_SMALL_CATEGORY = 0
INTENT_SMALL_CATEGORY = 1


def get_template_data(entity_large_category, entity_small_category, entity, intent):
    for data_item in read_txt(entity_large_category):
        if data_item[ENTITY_SMALL_CATEGORY] == entity_small_category and data_item[INTENT_SMALL_CATEGORY] == intent:
            print(data_item)
    return False
