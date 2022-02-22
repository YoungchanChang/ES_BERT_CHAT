

# 동작 로직

1. mecab_ner로부터 요청 받음
2. 카테고리에 따라 문장 bert_classifier에 삽입

# From mecab_ner

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