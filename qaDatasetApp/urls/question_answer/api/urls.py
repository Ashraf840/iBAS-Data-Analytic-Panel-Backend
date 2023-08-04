from django.urls import path, include
from qaDatasetApp.views.question_answer.api import question_answer_crud as qacrud

qa_api_name = 'QADatasetAppQuesAnsAPIEntries'

urlpatterns = [
    # [Answer APIs]
    # path("", qacrud.AnswerList.as_view(), name="AnswerList"),
    path('answer/', include(('qaDatasetApp.urls.question_answer.api.answer.urls', 'answer_api_name'),
                            namespace='QADatasetAppAnswerAPIEntries')),

    # [Question APIs]
    # path("", qacrud.QuestionList.as_view(), name="QuestionList"),
    path('question/', include(('qaDatasetApp.urls.question_answer.api.question.urls', 'question_api_name'),
                              namespace='QADatasetAppQuestionAPIEntries')),

    path('test-list/', qacrud.test_list, name='test'),
]
