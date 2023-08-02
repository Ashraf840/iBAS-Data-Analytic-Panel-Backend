from django.urls import path
from qaDatasetApp.views.question_answer.api import question_answer_crud as qacrud

qa_api_name = 'QADatasetAppQuesAnsAPIEntries'

urlpatterns = [
    path("id/<int:pk>/", qacrud.AnswerDetail.as_view(), name="AnswerDetail"),
    path("language/<str:language>/", qacrud.AnswerDetail.as_view(), name="AnswerDetail"),
    path("created-by/<str:created_by>/", qacrud.AnswerDetail.as_view(), name="AnswerDetail"),

    path('test-list/', qacrud.test_list, name='test'),
]