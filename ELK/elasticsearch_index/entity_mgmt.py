# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch

# ref : https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html

local_ip = "127.0.0.1"
es_port = "9200"

es = Elasticsearch(
    hosts=[
            {'host': local_ip, 'port': es_port, "timeout": 120, "max_retries": 10, "retry_on_timeout": True},
           ]
)

elastic_index = "mecab_entity"

def set_entity_index():

    result = es.indices.delete(index=elastic_index, ignore=[400, 404])
    print(result)
    body = {
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "nori_analyzer": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer",
                            "filter": [
                            ]
                        },
                    },
                }
            }
        },
        "mappings": {
            "properties": {
                "large_category": {
                    "type": "keyword"
                },
                "small_category": {
                    "type": "keyword"
                },
                "entity": {
                    "type": "text",
                    "analyzer": "nori_analyzer"
                },
                "mecab_parse": {
                    "type": "keyword"
                },
            }
        }
    }

    ans = es.indices.create(index=elastic_index, body=body, ignore=400, )
    print(ans)

if __name__ == "__main__":
    # print("한번 더 확인 요망. 저장된 데이터 많음")
    set_entity_index()
