import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync

class ChatConsumer(AsyncWebsocketConsumer):
    # chat start
    async def connect(self):
        # URL 루트 -> 방이름 확인 : consumer에게 웹소켓 연결을 엶
        self.room_name = self.scope['url_route']['kwargs']['user_pk']
        self.store_name = self.scope['url_route']['kwargs']['store_pk']
        # 그룹생성
        self.room_group_name = 'chat_%s' % self.room_name

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
        message = text_data_json['message']
        sender = text_data_json['name']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'name': sender,
                'message': message
            }
        )
    
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        name = event['name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'name': name,
            'message': message
        }))