

1. 주소 변경
mecab_ner=http://localhost:9090/mecab_entity
to
mecab_ner=http://mecab_ner:9090/mecab_entity

2. html 변경
templates/chats/room.html 변경
- FROM : ws://window.location.host/ws/chat/roomName/
- TO : ws://window.location.host/ws/chat/roomName/

4. 포트 변경