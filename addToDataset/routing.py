from django.urls import re_path, path
from .consumers import (
    generate_suggestive_question_loading_status as gsqls,
)


websocket_urlpatterns = [
    path('ws/data-seggregator/loading/status/', gsqls.GenerateSuggestiveQuestionLoadingStatusConsumer.as_asgi()),
]