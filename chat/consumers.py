from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.http import HttpResponse, HttpResponseNotFound
import json
import asyncio

from .models import Room


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        try:
            room_name = self.scope['url_route']['kwargs']['room_name']
            room_obj = await self.get_room(room_name)
            chat_room = room_obj.name
            self.chat_room = chat_room
            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )

            await self.send({
                "type": "websocket.accept",
            })

        except Room.DoesNotExist:
            return HttpResponseNotFound('<h1>Room not found</h1>')

    async def websocket_receive(self, event):
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat_message",
                "text": json.loads(event["text"]).get('message')
            }
        )

    async def chat_message(self, event):
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @database_sync_to_async
    def get_room(self, name):
        return Room.objects.get_or_create(name=name)[0]
