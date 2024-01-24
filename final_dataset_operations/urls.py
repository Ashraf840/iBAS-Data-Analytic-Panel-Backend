from django.urls import path
from . import views

urlpatterns = {
    path('get-final-dataset/', views.get_final_dataset_data, name = 'get_final_dataset_data'),
    path('add-to-dataset/', views.add_to_dataset, name = 'add_to_dataset'),
    path('clean-database-table/', views.clean_database_table, name = 'clean_database_table'),
    path('start-training/', views.start_training, name = 'start_training'),
    path('create-dataset/', views.create_dataset, name = 'create_dataset'),
}   
