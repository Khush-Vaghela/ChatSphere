import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Room, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']  # Changed from room_name
        self.room_group_code = f'chat_{self.room_code}'  # Changed from room_group_name

        await self.channel_layer.group_add(
            self.room_group_code,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_code,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        await self.save_message(user, self.room_code, message)

        await self.channel_layer.group_send(
            self.room_group_code,
            {
                'type': 'chat_message',
                'message': message,
                'username': user.username
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @database_sync_to_async
    def save_message(self, user, room_code, message):  # Changed from room_name
        room = Room.objects.get(code=room_code)
        Message.objects.create(room=room, user=user, content=message)