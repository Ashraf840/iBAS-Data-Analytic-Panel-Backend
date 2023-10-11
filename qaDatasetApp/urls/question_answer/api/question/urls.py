from django.urls import path
# from qaDatasetApp.views.question_answer.api import question_answer_crud as qacrud
from qaDatasetApp.views.question_answer.api.question import question_crud as qcrud

question_api_name = 'QADatasetAppQuesAPIEntries'

urlpatterns = [
    # [Question APIs]
    path("", qcrud.QuestionList.as_view(), name="QuestionList"),
    path("id/<int:pk>/", qcrud.QuestionDetail.as_view(), name="QuestionDetail"),
]