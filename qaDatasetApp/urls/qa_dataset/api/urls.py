from django.urls import path
from qaDatasetApp.views.qa_dataset.api import qa_dataset_crud as qadcrud
# from qaDatasetApp.views.question_answer.api import question_answer_crud

qa_dataset_api_name = 'QADatasetAppQADsetAPIEntries'

urlpatterns = [
    path('', qadcrud.QADatasetList.as_view(), name='QADatasetList'),
    path("id/<int:pk>/", qadcrud.QADatasetDetail.as_view(), name="QuestionDetail"),

    path('test-list/', qadcrud.test_list, name='test'),
]