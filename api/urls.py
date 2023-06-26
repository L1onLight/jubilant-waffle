from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_routes),
    path('add-post/', views.add_todo, name="addPost"),
    path('edit-todo/', views.edit_todo, name="editTodo"),

    path('folders/', views.user_todo_folder_list, name="folderList"),
    path('add-post-f/<folder_name>/',
         views.create_todo_infolder, name="addTodoInfolder"),
    path('edit-cb/<str:pk>/<bool_type>/', views.edit_cb, name="edit_cb"),
    path('create-folder/', views.create_folder, name="create_folder"),
    path('delete-todo/<str:pk>/', views.delete_todo, name="delete_todo"),
    path('add-to-folder/<str:folder_pk>/<str:todo_pk>/',
         views.add_to_folder, name="delete_todo"),
    path('delete-folder/<str:pk>/', views.delete_folder, name="delete_folder"),

]
