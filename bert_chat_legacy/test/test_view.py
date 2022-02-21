
from bert_control_dir.bert_mgmt import get_template_data

req_data = {'sender': 'youngchan', 'query': '나는 닭 튀김이 먹고 싶어', 'entity_large_category': 'food',
            'entity_small_category': 'fastfood', 'entity': '닭튀김', 'intent_large_category': 'food',
            'intent_small_category': 'eat', 'intent': '먹고 싶다'}


def test_endpoint_success():
    entity_large_category = 'food'
    entity_small_category = 'fastfood'
    entity = '닭튀김'
    intent_large_category = 'food'
    intent_small_category = 'eat'
    intent = '먹고 싶다'
    template_data = get_template_data(entity_large_category, entity_small_category, entity, intent_small_category)
    assert template_data is not False


def test_endpoint_fail():
    entity_large_category = 'food'
    entity_small_category = 'fastfood'
    entity = '닭튀김'
    intent_large_category = 'food'
    intent_small_category = 'wrong_data'
    intent = '먹고 싶다'
    template_data = get_template_data(entity_large_category, entity_small_category, entity, intent_small_category)
    assert template_data == False