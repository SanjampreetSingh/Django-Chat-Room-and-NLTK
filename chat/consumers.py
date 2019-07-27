from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.http import HttpResponse, HttpResponseNotFound
import json
import asyncio

from .models import Room

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })
        try:
            room_name = self.scope['url_route']['kwargs']['room_name']
            room_obj = await self.get_room(room_name)
            print(room_obj)
        except Room.DoesNotExist:
            return HttpResponseNotFound('<h1>Room not found</h1>')

    async def websocket_receive(self, event):
        await self.send({
            "type": "websocket.send",
            "text": json.loads(event["text"]).get('message'),
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def get_room(self, name):
        return Room.objects.get(name=name).name
