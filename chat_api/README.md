

# 동작 로직

1. chat_middleware에서 요청 받음
2. 카테고리에 따라 api서버 응답 요청.
3. api서버 응답 바탕으로 템플릿에 답변 만들어서 반환

# From chat_middleware

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
