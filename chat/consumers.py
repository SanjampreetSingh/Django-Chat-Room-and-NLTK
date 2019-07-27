from channels.consumer import AsyncConsumer

import json
import asyncio


class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        await self.send({
            "type": "websocket.send",
            "text": json.loads(event["text"]).get('message'),
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)
