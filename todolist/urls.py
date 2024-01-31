from django.urls import path
from .views import task_list, create_task

app_name = 'todolist'

urlpatterns = [
    path('tasks/', task_list, name='task_list'),
    path('create_task/', create_task, name='create_task'),
]
