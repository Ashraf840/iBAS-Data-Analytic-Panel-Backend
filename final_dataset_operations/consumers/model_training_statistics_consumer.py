from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json
import requests



# Customer Support Visitor Chat Consumer
class ModelTrainingStatisticsConsumer(WebsocketConsumer):
    
    def __init__(self, *args, **kwargs):
        super(ModelTrainingStatisticsConsumer, self).__init__(*args, **kwargs)
        # self.room_name = None
        self.room_group_name = None
    
    def connect(self):
        print("#"*50)
        print("[connect() method] Connected to backend consumer class: ModelTrainingStatisticsConsumer")
        # self.room_name = self.scope['url_route']['kwargs']['user_email']    # TODO: After implementing JWT token, verify if the user is an admin, otherwise, don't create a channel for staff users. Indeed, it'll be rest assured in the RestAPI endpoint of "get_final_dataset_data" view
        # self.room_group_name = 'mt_stat_socket_%s' % self.room_name     # THIS pattern is required to sent any asynchrobous msg to this consumer-channel
        self.room_group_name = 'mt_stat_socket'
        # print(f"room name: {self.room_name}")
        print(f"room-group name: {self.room_group_name}")
        print(f'Channel name: {self.channel_name}')
        

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name  # channels automatically fixes room-name?
        )
        async_to_sync(self.accept())
        print("#"*50)

    def receive(self, text_data=None, bytes_data=None):
        print("#"*50)
        print("[connect() method] Connected to backend consumer class: ModelTrainingStatisticsConsumer")
        data = json.loads(text_data)
        
        print("Received from frontend websocket:", data)

        print("#"*50)

    def disconnect(self, *args, **kwargs):
        print("#"*50)
        
        async_to_sync (self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        print("[disconnect() method] Disconnected from backend consumer class: ModelTrainingStatisticsConsumer")
        print("#"*50)
