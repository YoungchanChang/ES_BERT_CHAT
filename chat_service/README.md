

# chat_service logic
1. user_request를 chat_middleware에 보낸다.

## mecab_service
2. chat_middleware는 먼저 mecab_ner_app에 user_request를 보낸다.

3. mecab_ner_app는 user_request를 가공하여 ChatApiRequest형태로 bert_confirm app에 보낸다.

4. bert_confirm app는 데이터를 확인한 후 적절하면 true, 아니면 false로 변경한다. ChatApiRequest형태로 반환한다.

5. chat_middleware는 ChatApiRequest형태로 값을 받는다.

## chat_api_service

6. chat_middlewares는 ChatApiRequest형태로 chat_api_middleware에 보낸다.

7. chat_api_middleware는 ChatApiRequest형태에서 필요한 정보를 취하고 각 api 서버에 보낸다.

8. api서버에서 돌아오는 값을 조합하여 문장을 만든다.

9. 값을 반환한다.