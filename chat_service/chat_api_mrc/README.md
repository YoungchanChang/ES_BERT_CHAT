
# 동작 로직

1. chat_api에서 요청 받음
2. SearchAPI에 데이터 요청
3. SearchAPI에서 온 데이터를 MRC에 삽입
4. MRC답변 정제 후 response

# From chat_api To chat_api_mrc

RequestAPI:

- chat_middleware 컨테이너 -> chat_api_mrc 컨테이너에 응답 요청
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

- chat_middleware 컨테이너 <- chat_api_mrc 컨테이너에 응답

| 파라미터                 | 타입        | 필수여부 | 설명          |
|----------------------|-----------|------|-------------|
| api_template         | string    | Y    | 챗봇 템플릿 응답   |
| api_server           | string    | Y    | 응답 API서버 종류 |
| system_response_time | timefield | Y    | 시스템 응답 시간   |