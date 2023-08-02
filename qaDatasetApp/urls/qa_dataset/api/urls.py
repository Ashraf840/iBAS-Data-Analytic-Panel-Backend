from django.urls import path
from qaDatasetApp.views.qa_dataset.api import qa_dataset_crud
# from qaDatasetApp.views.question_answer.api import question_answer_crud

qa_dataset_api_name = 'QADatasetAppQADsetAPIEntries'

urlpatterns = [
    path('test-list/', qa_dataset_crud.test_list, name='test'),
]