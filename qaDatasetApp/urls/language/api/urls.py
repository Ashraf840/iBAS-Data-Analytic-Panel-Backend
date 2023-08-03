from django.urls import path
# from ....views.language.api import language_crud
# from ....views.language.api import language_crud
from qaDatasetApp.views.language.api import language_crud as lcrud

lang_api_name = 'QADatasetAppLangAPIEntries'

urlpatterns = [
    path("", lcrud.LanguageList.as_view(), name="LanguageList"),
    path("id/<int:pk>/", lcrud.LanguageDetail.as_view(), name="LanguageDetail"),
    path("name/<str:language_name>/", lcrud.LanguageDetail.as_view(), name="LanguageDetail"),

    path('test-list/', lcrud.test_list, name='test'),
]