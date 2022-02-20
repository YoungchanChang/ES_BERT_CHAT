

# 동작 로직

1. django_web에서 request 받음.
2. mecab_ner에 응답 요청
3. mecab_ner응답 바탕으로 chat_api서버에 응답 요청

# 1. From django_web container

- 장고웹 컨테이너로부터 받는 요청

RequestAPI:

| 파라미터         | 타입        | 필수여부 | 설명        |
|--------------|-----------|------|-----------|
| sentence     | string    | Y    | 사용자 발화 문장 |
| ip_info      | ip        | Y    | 사용자 ip정보  |
| request_time | timefield | Y    | 사용자 요청 시간 |

- 장고웹 컨테이너에 응답

ResponseAPI:

| 파라미터          | 타입        | 필수여부 | 설명       |
|---------------|-----------|------|----------|
| answer        | string    | Y    | 챗봇 응답 문장 |
| response_time | timefield | Y    | 챗봇 응답 시간 |


# 2. To mecab_ner

- mecab_ner컨테이너에 요청

RequestAPI:

| 파라미터            | 타입             | 필수여부 | 설명        |
|-----------------|----------------|--------|-----------|
| sentence        | string         | Y      | 사용자 발화 문장 |
| request_time    | timefield      | Y      | 시스템 요청 시간 |

- mecab_ner컨테이너에 응답

ResponseAPI:

| 파라미터                   | 타입             | 필수여부 | 설명             |
|------------------------|----------------|------|----------------|
| sentence               | string         | Y    | 사용자 발화 문장      |
| single                 | boolean        | Y    | 엔티티-인텐트 하나 여부  |
| chat_objects           | ArrayOfObjects | Y    | 엔티티-인텐트 포함 객체  |
| chat_objects 속성        | -              | -    | -              |
| split_sentence         | string         | Y    | 사용자 발화 문장      |
| all_category           | string         | N    | 엔티티-인텐트 대 카테고리 |
| entity                 | string         | N    | 추출 엔티티         |
| entity_medium_category | string         | N    | 엔티티 중 카테고리     |
| entity_small_category  | string         | N    | 엔티티 소 카테고리     |
| intent                 | string         | N    | 추출 인텐트         |
| intent_medium_category | string         | N    | 인텐트 중 카테고리     |
| intent_small_category  | string         | N    | 인텐트 소 카테고리     |
| bert_confirm           | boolean        | Y    | 버트 확인여부        |
| response_time          | timefield      | Y    | 시스템 응답 시간      |

# 3. To chat_api

- chat_api컨테이너에 요청. chat_objects의 하나씩 응답 요청

RequestAPI:

| 파라미터                   | 타입        | 필수여부 | 설명             |
|------------------------|-----------|------|----------------|
| sentence               | string    | Y    | 사용자 발화 문장      |
| all_category           | string    | N    | 엔티티-인텐트 대 카테고리 |
| entity                 | string    | N    | 추출 엔티티         |
| entity_medium_category | string    | N    | 엔티티 중 카테고리     |
| entity_small_category  | string    | N    | 엔티티 소 카테고리     |
| intent                 | string    | N    | 추출 인텐트         |
| intent_medium_category | string    | N    | 인텐트 중 카테고리     |
| intent_small_category  | string    | N    | 인텐트 소 카테고리     |
| bert_confirm           | boolean   | Y    | 버트 확인여부        |
| request_time           | timefield | Y    | 시스템 요청 시간      |



ResponseAPI:

| 파라미터          | 타입        | 필수여부 | 설명          |
|---------------|-----------|------|-------------|
| answer        | string    | Y    | 챗봇 템플릿 응답   |
| api_server    | string    | Y    | 응답 API서버 종류 |
| response_time | timefield | Y    | 시스템 응답 시간   |
