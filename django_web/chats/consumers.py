# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from chats.api_docker import get_bot_response
import logging
formatter = "%(asctime)s.%(msecs)03d\t%(levelname)s\t[%(name)s]\t%(message)s"
logging.basicConfig(level=logging.DEBUG, format=formatter, datefmt='%m/%d/%Y %I:%M:%S')

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        logging.warning({'message': self.scope['headers'][6]})
        await self.accept()
        await self.send(text_data=json.dumps({
            'message': "안녕!",
            'messenger': "FriendBot"
        }))

    async def disconnect(self, close_code):
        # Leave room group
        pass

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        messenger = text_data_json['messenger']

        print(message)
        # Send message to room group
        await self.send(text_data=json.dumps({
            'message': message,
            'messenger': messenger
        }))

        bot_response = str(get_bot_response(text_data))
        # Send message to room group
        await self.send(text_data=json.dumps({
            'message': bot_response,
            'messenger': "FriendBot"
        }))