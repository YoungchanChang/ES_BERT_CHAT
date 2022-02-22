

# 동작 로직

1. chat_middleware에서 요청 받음
2. 카테고리에 따라 api서버 응답 요청.
3. api서버 응답 바탕으로 템플릿에 답변 만들어서 반환

- api서버에 응답 요청시 chat_middleware에 보낸 spec으로 request 요청

# From chat_middleware To chat_api

RequestAPI:

- chat_middleware 컨테이너 -> chat_api 컨테이너에 응답 요청
- chat_objects의 하나씩 받음

| 파라미터                   | 타입        | 필수여부 | 설명             |
|------------------------|-----------|------|----------------|
| m_n_a                  | Objects   | Y    | 사용자 발화 문장      |
| req                    | Objects   | Y    | 사용자 발화 문장      |
| m_n_a속성                | -         | -    | -              |
| category_sentence      | string    | Y    | 사용자 발화 문장      |
| main_category          | string    | N    | 엔티티-인텐트 대 카테고리 |
| entity                 | string    | N    | 추출 엔티티         |
| entity_medium_category | string    | N    | 엔티티 중 카테고리     |
| entity_small_category  | string    | N    | 엔티티 소 카테고리     |
| intent                 | string    | N    | 추출 인텐트         |
| intent_medium_category | string    | N    | 인텐트 중 카테고리     |
| intent_small_category  | string    | N    | 인텐트 소 카테고리     |
| bert_confirm           | boolean   | Y    | 버트 확인여부        |
| req 속성                 | -         | -    | -              |
| user_sentence          | string    | Y    | 사용자 발화 문장      |
| user_ip                | ip        | Y    | 사용자 ip정보       |
| user_request_time      | timefield | Y    | 시스템 요청 시간      |


ResponseAPI:

- chat_middleware 컨테이너 <- chat_api 컨테이너에 응답

| 파라미터                 | 타입        | 필수여부 | 설명          |
|----------------------|-----------|------|-------------|
| api_response         | string    | Y    | 챗봇 템플릿 응답   |
| api_server           | string    | Y    | 응답 API서버 종류 |
| system_response_time | timefield | Y    | 시스템 응답 시간   |
