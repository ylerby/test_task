from django.urls import path
from test_task_app import views

urlpatterns = [
    path('index', views.CsvView.as_view()),
]
