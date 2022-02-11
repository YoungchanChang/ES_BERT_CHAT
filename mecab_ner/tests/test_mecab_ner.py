import mecab

from mecab_ner.app.application.service.mecab_parser import MeCabParser
from mecab_ner.app.application.service.mecab_storage import MeCabStorage
from mecab_ner.app.domain.entity import MecabWordFeature

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

    restore_sentence = MeCabStorage().get_reverse_parse(mecab_parse_results)

    assert len(restore_sentence) == 3


def test_gen_mecab_token_type_feature():

    mecab_parse_results = list(MeCabParser("나는 서울대병원에 갔어").gen_mecab_token_type_feature())

    assert len(mecab_parse_results) == 9

