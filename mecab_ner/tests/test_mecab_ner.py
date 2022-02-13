from typing import Generator

import mecab
from pathlib import Path

from mecab_ner.app.application.service.mecab_generator import MecabGenerator
from mecab_ner.app.application.service.mecab_ner import MeCabNer
from mecab_ner.app.application.service.mecab_parser import MeCabParser
from mecab_ner.app.application.service.mecab_storage import MeCabStorage
from mecab_ner.app.controller.service.mecab_controller import MeCabController
from mecab_ner.app.domain.entity import MecabWordFeature
from mecab_ner.app.utility.data_reader import DataReader

mecab = mecab.MeCab()


def test_python_mecab_parse():

    """ mecab parse 결과 테스트"""

    mecab_parse_nodes = mecab.parse("나는 서울대병원에 갔어")

    mecab_parse_list = []
    for node_surface, node_extract_feature in mecab_parse_nodes:
        mecab_parse_list.append(MecabWordFeature(node_surface, *node_extract_feature))

    for mecab_parse_item in mecab_parse_list:
        mecab_parse_item.idx_original = 0
        mecab_parse_item.mecab_token_idx = 0

    assert len(mecab_parse_list) == 7


def test_gen_mecab_token_feature():

    mecab_parse_results = list(MeCabParser("나는 서울대병원에 갔어").gen_mecab_token_feature())

    assert len(mecab_parse_results) == 7

    restore_sentence = MeCabStorage().restore_mecab_tokens(mecab_parse_results)

    assert len(restore_sentence) == 3


def test_gen_mecab_token_type_feature():

    mecab_parse_results = list(MeCabParser("나는 서울대병원에 갔어").gen_mecab_compound_token_feature())

    assert len(mecab_parse_results) == 9

    restore_sentence = MeCabStorage().reverse_compound_tokens(mecab_parse_results)

    assert len(restore_sentence) == 3


def test_read_category():
    storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/storage"

    # clear data
    m_g = MecabGenerator(storage_path=storage_path)
    for path_item in Path(m_g.mecab_path).iterdir():
        Path(path_item).unlink()
    Path(m_g.mecab_path).rmdir()

    # init data
    m_g = MecabGenerator(storage_path=storage_path)

    for data_item in m_g.gen_all_mecab_category_data(m_g.storage_path, need_parser=True):
        large_category, medium_category, data_dict = data_item

        assert isinstance(large_category, str)
        assert isinstance(medium_category, str)
        assert isinstance(data_dict, dict)

    m_g.write_category()


def test_read_intent_category():
    storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/intents/storage"

    # clear data
    m_g = MecabGenerator(storage_path=storage_path)
    for path_item in Path(m_g.mecab_path).iterdir():
        Path(path_item).unlink()
    Path(m_g.mecab_path).rmdir()

    # init data
    m_g = MecabGenerator(storage_path=storage_path)

    for data_item in m_g.gen_all_mecab_category_data(m_g.storage_path, need_parser=True):
        large_category, medium_category, data_dict = data_item

        assert isinstance(large_category, str)
        assert isinstance(medium_category, str)
        assert isinstance(data_dict, dict)

    m_g.write_category()


def test_storage_same():

    """ mecab 저장 데이터와 storage 데이터의 길이가 같은지 확인 """

    storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/storage"

    for path_item in Path(storage_path).iterdir():
        stroage_data_len = len(DataReader.read_txt(path_item))
        mecab_path_read = Path(storage_path).parent.joinpath(MecabGenerator.MECAB_STORAGE, path_item.name)
        mecab_data_len = len(DataReader.read_txt(mecab_path_read))
        assert stroage_data_len == mecab_data_len


def test_mecab_ner():
    """간단한 문장에서 엔티티 추출"""
    sentence = "나는 딸기가 먹고 싶어"
    entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/mecab_storage"
    mecab_ner = MeCabNer(storage_mecab_path=entity_storage_path)

    for mecab_category_item in mecab_ner.get_entities(sentence=sentence):

        assert mecab_category_item.large_category == "food"
        assert mecab_category_item.medium_category == "fruit"
        assert mecab_category_item.small_category == "#과일"
        assert mecab_category_item.entity == "딸기"

    intent_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/intents/mecab_storage"
    mecab_ner_intents = MeCabNer(storage_mecab_path=intent_storage_path)

    for mecab_intent_category_item in mecab_ner_intents.get_entities(sentence=sentence):
        assert mecab_intent_category_item.large_category == "food"
        assert mecab_intent_category_item.medium_category == "eat"
        assert mecab_intent_category_item.small_category == "#먹고 싶다"
        assert mecab_intent_category_item.entity == "먹 고 싶"


def test_infer_mecab_ner():
    sentence = "나는 신촌 딸기가 먹고 싶어"
    entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/mecab_storage"
    mecab_ner = MeCabNer(storage_mecab_path=entity_storage_path)

    for mecab_category_item in mecab_ner.get_entities(sentence=sentence, status=MeCabNer.INFER_FORWARD):
        assert mecab_category_item.large_category == "food"
        assert mecab_category_item.medium_category == "fruit"
        assert mecab_category_item.small_category == "#과일"
        assert mecab_category_item.entity == "신촌 딸기"


def test_infer_backward():
    sentence = "나는 라떼 한 잔이 먹고 싶어"
    entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/mecab_storage"
    mecab_ner = MeCabNer(storage_mecab_path=entity_storage_path)

    for mecab_category_item in mecab_ner.get_entities(sentence=sentence, status=MeCabNer.INFER_BACKWARD):
        assert mecab_category_item.large_category == "food"
        assert mecab_category_item.medium_category == "tea"
        assert mecab_category_item.small_category == "#차"
        assert mecab_category_item.entity == "라떼 한 잔"


def test_filter_entity():
    sentence = "나는 스윗한 딸기 치킨 먹고 싶어 사두감도 먹고 싶어"
    entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/mecab_storage"
    mecab_ner = MeCabNer(storage_mecab_path=entity_storage_path)
    entity_list = mecab_ner.gen_integrated_entities(sentence, status=MeCabNer.INFER_FORWARD)
    entity_list = list(entity_list)
    assert entity_list[0].large_category == "food"
    assert entity_list[0].medium_category == "fastfood"
    assert entity_list[0].small_category == "#패스트 푸드"
    assert entity_list[0].entity == "스윗한 딸기 치킨"

    assert entity_list[1].large_category == "food"
    assert entity_list[1].medium_category == "fruit"
    assert entity_list[1].small_category == "#과일"
    assert entity_list[1].entity == "사두감"

    sentence = "나는 딸기랑 감이 먹고 싶어"
    entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/mecab_storage"
    mecab_ner = MeCabNer(storage_mecab_path=entity_storage_path)
    entity_list = mecab_ner.gen_integrated_entities(sentence, status=MeCabNer.INFER_FORWARD)
    entity_list = list(entity_list)
    assert entity_list[0].large_category == "food"
    assert entity_list[0].medium_category == "fruit"
    assert entity_list[0].small_category == "#과일"
    assert entity_list[0].entity == "딸기"

    assert entity_list[1].large_category == "food"
    assert entity_list[1].medium_category == "fruit"
    assert entity_list[1].small_category == "#과일"
    assert entity_list[1].entity == "감"


def test_word_sense_disambiguation():
    sentence = "나는 차가 좋다"
    entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/entities/mecab_storage"
    mecab_ner = MeCabNer(storage_mecab_path=entity_storage_path)
    entity_list = mecab_ner.gen_integrated_entities(sentence, status=MeCabNer.INFER_FORWARD)
    entity_list = list(entity_list)
    assert len(entity_list) == 2

    entity_storage_path = "/Users/youngchan/Desktop/ES_BERT_CHAT/mecab_ner/datas/intents/mecab_storage"
    mecab_ner = MeCabNer(storage_mecab_path=entity_storage_path)
    intent_list = mecab_ner.gen_integrated_entities(sentence, status=MeCabNer.ENTITY)
    intent_list = list(intent_list)
    assert len(intent_list) == 3
