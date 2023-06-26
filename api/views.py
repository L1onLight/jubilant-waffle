from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.models import Todo, TodoFolders
from django.utils import timezone
from .decorators import *
from .serializers import *
from django.db import IntegrityError

# Create your views here.


@api_view(["GET"])
def get_routes(request):
    """Returns rest_framework response with paths for api."""

    routes = [
        'GET /api',
        'POST /api/add-post/',
        'GET /api/edit_cb/<str:pk>/<true|false>',
        'POST /api/add-post/',
        'POST /api/add-post/',
        # 'GET',
    ]

    return Response(routes)


@login_required_api
@api_view(["GET"])
def user_todo_folder_list(request):
    """Returns folder id, title and list of todo id's inside folder. Requires user."""
    folders = FolderSerializer(
        TodoFolders.objects.filter(user=request.user).all(), many=True)
    return Response(folders.data)


@login_required_api
@api_view(["POST"])
def add_todo(request):
    """Creates todo. 
    Requires user and title, datetime field optional"""
    if request.POST.get("todoInput") != '':
        try:
            new_todo = Todo(user=request.user,
                            title=request.POST.get("todoInput"))
            if request.POST.get("date"):
                new_todo.until = request.POST.get("date")
                print(1, request.POST.get("date"))
                print(2, new_todo.until)
            new_todo.save()
            return Response({"message": "Ok", "pk": new_todo.pk})
        except Todo.DoesNotExist:
            return Response({'message': "Not found."}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'message': "Some fields empty."}, status=status.HTTP_400_BAD_REQUEST)


@login_required_api
@api_view(["POST"])
def edit_todo(request):
    """Edits todo.
    Requires user, todo pk and new body from request"""
    pk = request.POST.get('id')
    body = request.POST.get("editTodo")
    try:
        todo_edit = Todo.objects.get(pk=pk, user=request.user)
    except Todo.DoesNotExist:
        return Response({'message': "Not found."}, status=status.HTTP_404_NOT_FOUND)
    if body != todo_edit.title:
        todo_edit.title = body
        todo_edit.save()
    return Response({"message": "Ok"})


@login_required_api
@api_view(["POST"])
def create_todo_infolder(request, folder_name):
    """Creates todo inside folder. 
    Requires user and title, datetime field optional"""
    try:
        tf = TodoFolders.objects.get(
            folder_title=folder_name, user=request.user)
        if request.POST.get("todoInput") != '':
            new_todo = Todo(user=request.user,
                            title=request.POST.get("todoInput"))
        else:
            return Response({'message': "Some fields empty."}, status=status.HTTP_400_BAD_REQUEST)
        if request.POST.get("date"):
            new_todo.until = request.POST.get("date")
        new_todo.save()
        tf.todo_list.add(new_todo)
        return Response({"message": "Ok", 'pk': new_todo.pk})
    except TodoFolders.DoesNotExist:
        return Response({'message': "Not found."}, status=status.HTTP_404_NOT_FOUND)


@login_required_api
@api_view(["GET"])
def edit_cb(request, pk, bool_type):
    """Change completed status. Required pk and true/false for changing. 
    Does not trigger save function if status == status from request."""
    try:
        todo = Todo.objects.get(pk=pk, user=request.user)
        state = True if bool_type == 'true' else False
        if state != todo.completed:
            todo.completed = state
            todo.save()
        return Response({"message": "Ok"})
    except Todo.DoesNotExist:
        return Response({'message': "Not found."}, status=status.HTTP_404_NOT_FOUND)


@login_required_api
@api_view(["POST"])
def create_folder(request):
    """Creates folder. Requires folder title and user."""
    title = request.data.get("folderTitle")
    if title == '':
        return Response({'message': "Some fields empty."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        nt = TodoFolders(user=request.user, folder_title=title)
        nt.save()
        return Response({"message": "Ok"})
    except TodoFolders.DoesNotExist:
        return Response({'message': "Not found."}, status=status.HTTP_404_NOT_FOUND)
    except IntegrityError as e:
        if "UNIQUE constraint failed" in str(e):
            return Response({'message': "Folder title should be unique."}, status=status.HTTP_402_PAYMENT_REQUIRED)


@login_required_api
@api_view(["GET"])
def delete_folder(request, pk):
    """Deletes folder. 
    Requires user and pk."""
    try:
        f_td = TodoFolders.objects.get(user=request.user, pk=pk)
        f_td.delete()
        print(f'{f_td} deleted')
        return Response({"message": "Ok"})
    except TodoFolders.DoesNotExist:
        return Response({'message': "Not found."}, status=status.HTTP_404_NOT_FOUND)


@login_required_api
@api_view(["GET"])
def delete_todo(request, pk):
    """Deletes Todo.
    Requires user and pk."""
    try:
        to_delete = Todo.objects.get(pk=pk, user=request.user)
        to_delete.delete()
        return Response({"message": "Ok"})
    except Todo.DoesNotExist:
        return Response({'message': "Not found."}, status=status.HTTP_404_NOT_FOUND)


@login_required_api
@api_view(["GET"])
def add_to_folder(request, folder_pk, todo_pk):
    # TODO make js function which sends request using folder name?
    """Adds Todo to folder.
    Requires user and folder <NAME/PK>"""
    print('tt')
    try:
        user = request.user
        todo = Todo.objects.get(pk=todo_pk, user=user)
        tf = TodoFolders.objects.get(pk=folder_pk, user=user)
        tf.todo_list.add(todo)
        # folder = TodoFolders.objects.get(pk=pk)
        return Response({"message": "Ok"})
    except Todo.DoesNotExist:
        return Response({'message': "Todo not found."}, status=status.HTTP_404_NOT_FOUND)
    except TodoFolders.DoesNotExist:
        return Response({'message': "Todo Folder not found."}, status=status.HTTP_404_NOT_FOUND)
