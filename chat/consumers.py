from channels.consumer import AsyncConsumer

import json
import asyncio


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })

        await self.send({
            "type": "websocket.send",
            "text": "Someone logged in"
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    async def websocket_receive(self, event):
        text_data = event.get('text', None)
        if text_data is not None:
            text_data_loaded = json.loads(text_data)
            message = text_data_loaded.get('message')
            
            await self.send({
                "type": "websocket.send",
                "message": message
            })
