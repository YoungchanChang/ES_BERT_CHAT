# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from chats.api_docker import get_mecab_ner


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']


        # Send message to room group
        await self.send(text_data=json.dumps({
            'message': message
        }))

        # Send message to room group
        await self.send(text_data=json.dumps({
            'message': str(get_mecab_ner(text_data))
        }))