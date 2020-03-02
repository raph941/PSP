import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ValidationError
from directmessages.signals import message_read, message_sent
from django.core import serializers


from directmessages.apps import Inbox
from directmessages.models import Message, ChatRoom
from accounts.models import User

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("connected", event)
        await self.send({       
            "type": "websocket.accept"
        })

    async def websocket_receive(self, event):
        print("recieved", event)

        front_data = event.get('text', None)
        if front_data is not None:
            loaded_dict_data = json.loads(front_data)
            sender_pk = loaded_dict_data.get("sender")
            recipient_pk = loaded_dict_data.get("reciever")
            message = loaded_dict_data.get("message")

            sender = await self.get_user(sender_pk)
            recipient = await self.get_user(recipient_pk)
            instance = await self.send_message(sender, recipient, message)
            sent_at = str(instance.sent_at)

            '''chat room'''
            chat_room_obj = await self.get_chat_room(sender, recipient)
            self.chat_room_obj = chat_room_obj
            print(sender, chat_room_obj)
            chat_room = f"chat_{chat_room_obj.id}"
            self.chat_room = chat_room

            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )

            myResponse = {
                'message': message,
                'sender': sender.pk,
                "recipient": recipient.pk,
                "sent_at": sent_at
            }

            #broadcasts the message event to be sent
            await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "chat_message",
                    "text": json.dumps(myResponse)
                }
            )
        
    async def chat_message(self, event):
        #sends the actual message
        await self.send({
            "type": "websocket.send",
            "text": event['text']
        })

    async def disconnect(self, event):
        #when the socket disconnects
        print("disconnected", event)
        await self.channel_layer.group_discard(self.chat_room, self.channel_name)

    @database_sync_to_async
    def get_conversation(self, user1, user2, limit=None, reversed=False, mark_read=False):
        users = [user1, user2]
        # Newest message first if it's reversed (index 0)
        if reversed:
            order = '-pk'
        else:
            order = 'pk'
        conversation = Message.objects.all().filter(sender__in=users, recipient__in=users).order_by(order)

        if limit:
            # Limit number of messages to the x newest
            conversation = conversation[:limit]

        if mark_read:
            for message in conversation:
                # Just to be sure, everything is read
                self.mark_as_read(message)

        return conversation

    @database_sync_to_async
    def send_message(self, sender, recipient, message):
        if sender == recipient:
            raise ValidationError("You can't send messages to yourself.")
        room, created = ChatRoom.objects.get_or_new(sender, recipient)

        message = Message(sender=sender, recipient=recipient, content=str(message), room=room)
        message.save()

        message_sent.send(sender=message, from_user=message.sender, to=message.recipient)

        # The second value acts as a status value
        return message

    @database_sync_to_async
    def get_user(self, pk):
        return User.objects.get(pk=pk)

    @database_sync_to_async
    def get_chat_room(self, user1, user2):
        return ChatRoom.objects.get_or_new(user1, user2)[0]