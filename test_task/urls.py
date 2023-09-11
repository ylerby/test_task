from django.urls import path
from test_task_app import views

urlpatterns = [
    path('index', views.CsvView.as_view()),
    path('', views.index),
    path('login', views.login),
    path('register', views.register)
]
