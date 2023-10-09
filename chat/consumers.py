import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model

from .serializers import MessageSerializer
from .models import Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        current_user_id = int(self.scope["query_string"])
        other_user_id = self.scope["url_route"]["kwargs"]["id"]
        self.room_name = (
            f"{current_user_id}_{other_user_id}"
            if int(current_user_id) > int(other_user_id)
            else f"{other_user_id}_{current_user_id}"
        )
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await super().disconnect(close_code)

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data["message"]
        sender_username = data["senderUsername"]
        reciever_username = data["receiverUsername"]
        sender = await self.get_user(sender_username)
        reciever = await self.get_user(reciever_username)

        await self.save_message(
            sender=sender, reciever=reciever, message=message, thread_name=self.room_group_name
        )

        messages = await self.get_messages()
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "senderUsername": sender_username,
                "messages": messages,
            },
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["senderUsername"]
        messages = event["messages"]

        await self.send(
            text_data=json.dumps(
                {
                    "message": message,
                    "senderUsername": username,
                    "messages": messages,
                }
            )
        )

    @database_sync_to_async
    def get_user(self, username):
        return get_user_model().objects.filter(email=username).first()

    @database_sync_to_async
    def get_messages(self):
        messages = []
        for instance in Message.objects.filter(thread_name=self.room_group_name):
            messages = MessageSerializer(instance).data
        return messages

    @database_sync_to_async
    def save_message(self, sender,reciever, message, thread_name):
        Message.objects.create(sender=sender, receiver=reciever, message=message, thread_name=thread_name)
