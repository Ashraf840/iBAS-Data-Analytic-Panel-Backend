from django.contrib import admin
from django.urls import path, include
from addToDataset.views import addToDataset, suggestiveQA, genSuggestiveQa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('qa-dataset/', include(('qaDatasetApp.urls.urls', 'app_name'), namespace='QADatasetApplication')),
    path('add-to-dataset/', addToDataset),
    path('suggestive-qa/', suggestiveQA),
    path('gen-suggestive-qa/', genSuggestiveQa),
]
