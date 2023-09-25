from django.urls import path
from test_task_app import views

urlpatterns = [
    path('index', views.index),
    path('download_csv_file', views.CsvView.as_view()),
    path('get_csv_file', views.GetCsvView.as_view()),
    path('file_sorting/', views.FileSorting.as_view()),
    path('delete_csv_file', views.DeleteCsvView.as_view()),
    path('get_all_files', views.get_all_files),
    path('', views.main_page),
    path('login', views.LoginView.as_view()),
    path('register', views.RegisterView.as_view()),
]
