from elasticsearch import Elasticsearch
from elasticsearch import helpers

from pathlib import Path
from chat_service.mecab_service.mecab_ner_app.app.application.service.mecab_reader import MecabDataController

local_ip = "127.0.0.1"
es_port = "9200"
elastic_index = "mecab_entity"

es = Elasticsearch(
    hosts=[
            {'host': local_ip, 'port': es_port, "timeout": 120, "max_retries": 10, "retry_on_timeout": True},
           ]
)

WORD = 0
MECAB = 1

python_mecab_ner_dir = Path(__file__).resolve().parent.joinpath("entity_data")


class ElasticMecabDataController(MecabDataController):
    MIN_MEANING = 2
    NER_POS = "entity"
    DUPLICATE = False
    START_IDX = False

    def _set_mecab_path(self, ner_path: str) -> None:
        ...


def gendata():
    m_g = ElasticMecabDataController(ner_path=str(python_mecab_ner_dir))
    for data_item in m_g.gen_all_mecab_category_data(m_g.ner_path, use_mecab_parser=True):
        category, content = data_item
        # 무조건 small_category는 있어야 한다.
        for content_key in content.keys():
            for content_item_of_item in content[content_key]:

                yield {
                    "_index": elastic_index,
                    "_source": {
                            "large_category": category,
                            "small_category": content_key,
                            "entity": content_item_of_item[WORD],
                            "mecab_parse": content_item_of_item[MECAB]
                        }
                }
helpers.bulk(es, gendata())