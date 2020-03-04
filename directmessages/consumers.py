import asyncio
import json
import datetime
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
        loaded_dict_data = json.loads(front_data)
        purpose = loaded_dict_data.get("purpose")
        
        if purpose == "input-click-event" or purpose == "hover-event":
            me = loaded_dict_data.get("me")
            other_guy = loaded_dict_data.get("other_guy")
            await self.mark_as_read_bulk(me, other_guy)
        elif purpose == "fullname-click-event":
            me = loaded_dict_data.get("me")
            other_guy = loaded_dict_data.get("other_guy")
            me = await self.get_user(me)
            other_guy = await self.get_user(other_guy)
            chat_room_obj = await self.get_chat_room(me, other_guy)
            self.chat_room_obj = chat_room_obj
            chat_room = f"chat_{chat_room_obj.id}"
            self.chat_room = chat_room
            print(me, chat_room_obj)

            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )
        else:
            if front_data is not None:
                sender_pk = loaded_dict_data.get("sender")
                recipient_pk = loaded_dict_data.get("reciever")
                message = loaded_dict_data.get("message")

                sender = await self.get_user(sender_pk)
                recipient = await self.get_user(recipient_pk)
                instance = await self.send_message(sender, recipient, message)
                sent_at = str(instance.sent_at)

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
            else:
                print(event)
        
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

    @database_sync_to_async
    def mark_as_read_bulk(self, me, other_guy):
        '''
        Note that me, and other_guy are integer fields representing the primary keys of the two fellas repectively
        '''
        me = User.objects.get(pk=me)
        other_guy = User.objects.get(pk=other_guy)
        unread_messages = Message.objects.all().filter(sender=other_guy, recipient=me, read_at=None)
        for msg in unread_messages:
            msg.read_at = datetime.datetime.now()
            msg.save()