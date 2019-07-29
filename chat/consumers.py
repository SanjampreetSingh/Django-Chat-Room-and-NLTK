from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.http import HttpResponse, HttpResponseNotFound
import json
import asyncio

from .models import Room, Message


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        try:
            room_name = self.scope['url_route']['kwargs']['room_name']
            room_obj = await self.get_room(room_name)
            self.room_obj = room_obj

            chat_room = room_name
            self.chat_room = chat_room
            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )

            await self.send({
                "type": "websocket.accept",
            })

            await self.join_message()

        except Room.DoesNotExist:
            return HttpResponseNotFound('<h1>Room not found</h1>')

    async def join_message(self):
       await self.channel_layer.group_send(
           self.chat_room,
           {
               "type": "join_messages",
               "text":  'Someone Joined'
           }
       )

    async def join_messages(self,event):
        await self.send({
            "type": "websocket.send",
            "text": "Someone Joined!"
        })


    async def websocket_receive(self, event):
        message = json.loads(event["text"]).get('message')
        await self.save_chat_message(message)
        await self.channel_layer.group_send(
            self.chat_room,
            {
                "type": "chat_message",
                "text": message
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

    @database_sync_to_async
    def save_chat_message(self, message):
        room_obj = self.room_obj
        return Message.objects.create(room=room_obj, message=message)
