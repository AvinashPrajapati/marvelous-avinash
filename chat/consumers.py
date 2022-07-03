import json
from re import U
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
# from django.contrib.auth.models import User
from .models import Message, CustomUser
from tutorials.models import Tutorial


class ChatComsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        self.close()
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        token = data['token']
        room = data['room']

        await self.save_message(message, token, room)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type':'chat_message',
                'message':message,
                'token':token,
                'room':room,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        token = event['token']
        room = event['room']

        await self.send(text_data=json.dumps({
            'message': message,
            'token': token,
            'room': room, 
        }))

    @sync_to_async
    def save_message(self, message, token, room):
        user = CustomUser.objects.get(token=token)
        room = Tutorial.objects.get(url=room)
        print("success ...")

        Message.objects.create(user = user, room=room, content = message)


