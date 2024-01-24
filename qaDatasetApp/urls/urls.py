from django.urls import path, include

app_name = 'QADatasetApp'

urlpatterns = [
    path('api/', include(('qaDatasetApp.urls.api', 'api_name'), namespace='QADatasetAppAPI')),
]
