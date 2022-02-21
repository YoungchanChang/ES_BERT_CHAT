

# 동작 로직

1. django_web에서 request 받음.
2. mecab_ner에 응답 요청
3. mecab_ner응답 바탕으로 chat_api서버에 응답 요청

# 1. From django_web container

RequestAPI:

- django_web 컨테이너 -> chat_middleware 컨테이너에 응답 요청

| 파라미터              | 타입        | 필수여부 | 설명        |
|-------------------|-----------|------|-----------|
| user_sentence     | string    | Y    | 사용자 발화 문장 |
| user_ip           | ip        | Y    | 사용자 ip정보  |
| user_request_time | timefield | Y    | 사용자 요청 시간 |

- django_web 컨테이너 <- chat_middleware 컨테이너에 응답

ResponseAPI:

| 파라미터                 | 타입        | 필수여부 | 설명        |
|----------------------|-----------|------|-----------|
| bot_response         | string    | Y    | 챗봇 응답 문장  |
| system_response_time | timefield | Y    | 시스템 응답 시간 |


# 2. To mecab_ner

RequestAPI:

- chat_middleware 컨테이너 -> mecab_ner 컨테이너에 응답 요청

| 파라미터              | 타입        | 필수여부 | 설명        |
|-------------------|-----------|------|-----------|
| user_sentence     | string    | Y    | 사용자 발화 문장 |
| user_ip           | ip        | Y    | 사용자 ip정보  |
| user_request_time | timefield | Y    | 사용자 요청 시간 |

ResponseAPI:

- chat_middleware 컨테이너 <- mecab_ner 컨테이너에 응답

| 파라미터                   | 타입             | 필수여부 | 설명                 |
|------------------------|----------------|------|--------------------|
| user_sentence          | string         | Y    | 사용자 발화 문장          |
| is_atomic              | boolean        | Y    | 엔티티-인텐트 하나 여부      |
| system_response_time   | timefield      | Y    | 시스템 응답 시간          |
| sentence_attributes    | ArrayOfObjects | Y    | 엔티티-인텐트 포함 객체      |
| sentence_attributes 속성 | -              | -    | -                  |
| category_sentence      | string         | Y    | 엔티티 많을 때 사용자 발화 문장 |
| main_category          | string         | N    | 엔티티-인텐트 대 카테고리     |
| entity                 | string         | N    | 추출 엔티티             |
| entity_medium_category | string         | N    | 엔티티 중 카테고리         |
| entity_small_category  | string         | N    | 엔티티 소 카테고리         |
| intent                 | string         | N    | 추출 인텐트             |
| intent_medium_category | string         | N    | 인텐트 중 카테고리         |
| intent_small_category  | string         | N    | 인텐트 소 카테고리         |
| bert_confirm           | boolean        | Y    | 버트 확인여부            |

# 3. To chat_api

RequestAPI:

- chat_middleware 컨테이너 -> chat_api 컨테이너에 응답 요청
- chat_objects의 하나씩 응답 요청

| 파라미터                   | 타입             | 필수여부 | 설명                 |
|------------------------|----------------|------|--------------------|
| req                    | Objects        | Y    | 사용자 발화 문장          |
| sentence_attributes    | ArrayOfObjects | Y    | 엔티티-인텐트 포함 객체      |
| is_atomic              | boolean        | Y    | 엔티티-인텐트 하나 여부      |
| req 속성                 | -              | -    | -                  |
| user_sentence          | string         | Y    | 사용자 발화 문장          |
| user_ip                | ip             | Y    | 사용자 ip정보           |
| user_request_time      | timefield      | Y    | 시스템 요청 시간          |
| sentence_attributes 속성 | -              | -    | -                  |
| category_sentence      | string         | Y    | 엔티티 많을 때 사용자 발화 문장 |
| main_category          | string         | N    | 엔티티-인텐트 대 카테고리     |
| entity                 | string         | N    | 추출 엔티티             |
| entity_medium_category | string         | N    | 엔티티 중 카테고리         |
| entity_small_category  | string         | N    | 엔티티 소 카테고리         |
| intent                 | string         | N    | 추출 인텐트             |
| intent_medium_category | string         | N    | 인텐트 중 카테고리         |
| intent_small_category  | string         | N    | 인텐트 소 카테고리         |
| bert_confirm           | boolean        | Y    | 버트 확인여부            |


ResponseAPI:

- chat_middleware 컨테이너 <- chat_api 컨테이너에 응답

| 파라미터                 | 타입        | 필수여부 | 설명          |
|----------------------|-----------|------|-------------|
| api_response         | string    | Y    | 챗봇 템플릿 응답   |
| api_server           | string    | Y    | 응답 API서버 종류 |
| system_response_time | timefield | Y    | 시스템 응답 시간   |
