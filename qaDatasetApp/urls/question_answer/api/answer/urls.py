from django.urls import path
from qaDatasetApp.views.question_answer.api.answer import answer_crud as acrud

answer_api_name = 'QADatasetAppAnsAPIEntries'

urlpatterns = [
    # [Answer APIs]
    path("", acrud.AnswerList.as_view(), name="AnswerList"),
    path("id/<int:pk>/", acrud.AnswerDetail.as_view(), name="AnswerDetail"),  # int-query by answer-id

    # ---------------- [by 'language-id' & 'user-id' ARE NOT ELIGIBLE, TURNED OFF, WILL BE USED WHILE USING DJANGO-FILTER]
    # path("language/<int:language>/", acrud.AnswerDetail.as_view(), name="AnswerDetail"),  # int-query by language-id
    # path("created-by/<int:created_by>/", acrud.AnswerDetail.as_view(), name="AnswerDetail"),
]