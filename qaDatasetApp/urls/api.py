from django.urls import path, include

api_name = 'QADatasetAppAPIEntries'

urlpatterns = [
    path('language/', include(('qaDatasetApp.urls.language.api.urls', 'lang_api_name'),
                              namespace='QADatasetAppLanguageAPIEntries')),
    path('question-answer/', include(('qaDatasetApp.urls.question_answer.api.urls', 'qa_api_name'),
                                     namespace='QADatasetAppQuestionAnswerAPIEntries')),
    path('qa-dataset/', include(('qaDatasetApp.urls.qa_dataset.api.urls', 'qa_dataset_api_name'),
                                namespace='QADatasetAppQADatasetAPIEntries')),
]
