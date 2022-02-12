import json
import datetime

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from allcake.settings import CLIENT

@database_sync_to_async
def save_to_database(db, collection, chat_message):
    print('inside save_to_database====>', db, collection, chat_message)
    r = CLIENT[db][collection].insert_one(chat_message)
    return (True, r.inserted_id)

class ChatConsumer(AsyncWebsocketConsumer):
    # chat start
    async def connect(self):
        # URL 루트 -> 방이름 확인 : consumer에게 웹소켓 연결을 엶
        self.room_name = self.scope['url_route']['kwargs']['user_pk']
        self.store_name = self.scope['url_route']['kwargs']['store_pk']

        # 그룹생성
        room = self.store_name + "_" + self.room_name
        self.room_group_name = 'chat_%s' % room

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    # chat end
    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        user_name = text_data_json['user_name']
        user_id = text_data_json['user_id']
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        message = text_data_json['message']

        chat_data = {'type' : 'chat_message', 'user_id':user_id,  'user_name':user_name,
            'message': message, 'timestamp':timestamp}
        
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            chat_data
        )

        # Save to DataBase
        room_name = self.scope['url_route']['kwargs']['store_pk']
        room_name += "_"
        room_name += self.scope['url_route']['kwargs']['user_pk']
        timestamp = datetime.datetime.utcnow()

        if message:
            chat_data = {'chat_room' : room_name, 'user_id':user_id,  'user_name':user_name,
            'message':{'text':message}, 'timestamp':timestamp}
            # Save
            status, inserted_id = await save_to_database('chat_message', 'account_1', chat_data)
            # Checking
            if status:
                print('chat saved to db successfully ====>', inserted_id)
            else:
                print('saving to db failed')

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))