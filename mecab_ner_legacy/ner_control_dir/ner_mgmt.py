from mecab_value_extractor_dir.test_dir.ner_intent_test import get_entity_intent

QUERY = 0
LARGE_CATEGORY = 1
SMALL_CATEGORY = 2
E_I_VAL = 3
ENTITY = 1
INTENT = 2


def get_entity_intent_dict(query):
    return_dict = {}
    entity_intent = get_entity_intent(query)
    if entity_intent:
        return_dict['query'] = entity_intent[QUERY]
        return_dict['entity_large_category'] = entity_intent[ENTITY][LARGE_CATEGORY]
        return_dict['entity_small_category'] = entity_intent[ENTITY][SMALL_CATEGORY]
        return_dict['entity'] = entity_intent[ENTITY][E_I_VAL]
        return_dict['intent_large_category'] = entity_intent[INTENT][LARGE_CATEGORY]
        return_dict['intent_small_category'] = entity_intent[INTENT][SMALL_CATEGORY]
        return_dict['intent'] = entity_intent[INTENT][E_I_VAL]
        return return_dict
    return False
