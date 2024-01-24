from django.urls import path
from qaDatasetApp.views.question_answer.api.answer import answer_crud as acrud

answer_api_name = 'QADatasetAppAnsAPIEntries'

urlpatterns = [
    # [Answer APIs]
    path("", acrud.AnswerList.as_view(), name="AnswerList"),
    path("id/<int:pk>/", acrud.AnswerDetail.as_view(), name="AnswerDetail"),  # int-query by answer-id
]