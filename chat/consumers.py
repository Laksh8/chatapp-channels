import json
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GroupChatConsumer(WebsocketConsumer):
    # Only Authenticated users allowed
    def connect(self):

        self.room_name = self.scope["url_route"]["kwargs"]["group_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))



class UserChatConsumer(WebsocketConsumer):
    def connect(self):
        
        # Check for Authentication
        # print("#################",self.scope["user"])
        if self.scope["user"].is_anonymous:
            self.close()
            return 
        
        # print("@@@@@@@@@@@@@@@@@@@@@@@@",self.scope['user'],dir(self.scope['user']))
        from_user = self.scope["user"]

        to_user = User.objects.filter(username=self.scope["url_route"]["kwargs"]["user_id"])
        # print(to_user)
        if not to_user.exists():
            self.close()
            return
        to_user = to_user.first()
        self.room_name = self.scope["url_route"]["kwargs"]["user_id"]
        # print("-".join(sorted([str(from_user.id), str(to_user.id)])))
        self.room_group_name = "-".join(sorted([str(from_user.id), str(to_user.id)]))
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        # try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )
        # except Exception as e:
        #     print(e)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # message = text_data_json

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message","data":text_data_json}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["data"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(event))