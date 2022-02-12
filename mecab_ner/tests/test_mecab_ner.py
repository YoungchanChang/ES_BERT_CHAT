from typing import Generator

import mecab
from pathlib import Path
from mecab_ner.app.application.service.mecab_parser import MeCabParser
from mecab_ner.app.application.service.mecab_storage import MeCabStorage
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

    for path_item in Path(storage_path).iterdir():

        txt_data = DataReader.read_txt(path_item)
        for data_item in DataReader.read_category(txt_data):
            title, contents = data_item

            assert isinstance(title, str)
            assert isinstance(contents, list)

            for content_item in contents:
                assert isinstance((MeCabParser(content_item).gen_mecab_compound_token_feature()), Generator)