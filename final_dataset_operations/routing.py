from django.urls import re_path, path
from .consumers import (
    model_training_statistics_consumer as mtsc,
)


websocket_urlpatterns = [
    path('ws/chatbot-model/training/statistics/', mtsc.ModelTrainingStatisticsConsumer.as_asgi()),
]