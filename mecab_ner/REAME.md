

# 동작 로직

1. chat_middleware로부터 응답 받음
2. 데이터 분석
3. 분석된 데이터 mecab_bert_confirm에 전달 후 응답

# From chat_middleware

- chat_middleware컨테이너에서 요청

RequestAPI:

| 파라미터            | 타입             | 필수여부 | 설명        |
|-----------------|----------------|--------|-----------|
| sentence        | string         | Y      | 사용자 발화 문장 |
| request_time    | timefield      | Y      | 시스템 요청 시간 |

- chat_middleware컨테이너에 응답

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

# To mecab_bert_confirm

- chat_middleware컨테이너에서 요청

RequestAPI:

| 파라미터            | 타입             | 필수여부 | 설명        |
|-----------------|----------------|--------|-----------|
| sentence        | string         | Y      | 사용자 발화 문장 |
| all_category           | string         | N    | 엔티티-인텐트 대 카테고리 |
| request_time    | timefield      | Y      | 시스템 요청 시간 |

- chat_middleware컨테이너에 응답

ResponseAPI:

| 파라미터                   | 타입             | 필수여부 | 설명             |
|------------------------|----------------|------|----------------|
| bert_confirm           | boolean        | Y    | 버트 확인여부        |
| response_time          | timefield      | Y    | 시스템 응답 시간      |