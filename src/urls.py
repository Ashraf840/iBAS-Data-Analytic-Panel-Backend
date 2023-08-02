from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('qa-dataset/', include(('qaDatasetApp.urls.urls', 'app_name'), namespace='QADatasetApplication')),
]
