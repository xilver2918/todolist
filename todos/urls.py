from django.urls import path #주소경로를 등록하는 path기능
from . import views #현재 폴더의 views.py를 가져와 

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("create/", views.todo_create, name="todo_create"),
    path(
        "<int:todo_id>/toggle/",
        views.todo_toggle,
        name="todo_toggle",
    ), # int:todo_id URL에서 정수값을 받아 View의 todo_id로 넘기겠다. 
     path(
        "<int:todo_id>/delete/",
        views.todo_delete,
        name="todo_delete",
    ),
] #이 주소에 접속하면 views.py의 todo_list 함수를 실행해라 