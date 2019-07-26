from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self, event):
        print('connected', event)
        self.accept()

    async def disconnect(self, close_code, event):
        print('disconnected', event, close_code)

    async def receive(self, text_data, event):
        print('recieved', event)
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
