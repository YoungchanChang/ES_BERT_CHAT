from mecab_value_extractor_dir.test_dir.ner_intent_test import get_entity_intent

QUERY = 0
ENTITY_LARGE_CATEGORY = 2
ENTITY_SMALL_CATEGORY = 3
ENTITY = 4
INTENT_LARGE_CATEGORY = 6
INTENT_SMALL_CATEGORY = 7
INTENT = 8


def get_entity_intent_dict(query):
    return_dict = {}
    if entity_intent := get_entity_intent(query):
        return_dict['query'] = entity_intent[QUERY]
        return_dict['entity_large_category'] = entity_intent[ENTITY_LARGE_CATEGORY]
        return_dict['entity_small_category'] = entity_intent[ENTITY_SMALL_CATEGORY]
        return_dict['entity'] = entity_intent[ENTITY]
        return_dict['intent_large_category'] = entity_intent[INTENT_LARGE_CATEGORY]
        return_dict['intent_small_category'] = entity_intent[INTENT_SMALL_CATEGORY]
        return_dict['intent'] = entity_intent[INTENT]
        return return_dict
    return False
