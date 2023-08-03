from django.urls import path
from qaDatasetApp.views.question_answer.api import question_answer_crud as qacrud

qa_api_name = 'QADatasetAppQuesAnsAPIEntries'

urlpatterns = [
    # [Answer APIs]
    path("", qacrud.AnswerList.as_view(), name="AnswerList"),
    path("id/<int:pk>/", qacrud.AnswerDetail.as_view(), name="AnswerDetail"),  # int-query by answer-id
    path("language/<int:language>/", qacrud.AnswerDetail.as_view(), name="AnswerDetail"),  # int-query by language-id
    path("created-by/<int:created_by>/", qacrud.AnswerDetail.as_view(), name="AnswerDetail"),

    # [Question APIs]
    path("", qacrud.QuestionList.as_view(), name="QuestionList"),
    path('test-list/', qacrud.test_list, name='test'),
]