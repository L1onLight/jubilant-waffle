from django.shortcuts import render, get_object_or_404, redirect
from user.forms import RegisterForm, CustomLoginForm
from .models import Todo, TodoFolders
from django.contrib.auth import logout
from .decorators import *
from django.contrib import messages
from .models import CustomUser
from django.http import QueryDict
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
# Pagination
from django.core.paginator import Paginator

# Create your views here.
PAGINATION_N = 7


@login_required_my
def home(request):
    todo_list = Todo.objects.filter(user=request.user)
    if "uncompleted" in request.GET:
        todo_list = todo_list.filter(completed=False)
    elif 'completed' in request.GET:
        todo_list = todo_list.filter(completed=True)

    todo_folders = TodoFolders.objects.filter(user=request.user)

    p = Paginator(todo_list, PAGINATION_N)
    page = request.GET.get('page')
    todo_list = p.get_page(page)
    print(p.count)
    context = {'todo_list': todo_list, "todo_folders": todo_folders, "paginator": p,
               'pn': PAGINATION_N}
    return render(request, 'core/index.html', context)


@login_required_my
def folder_page(request, folder_name):

    try:
        todo_list = TodoFolders.objects.get(
            folder_title=folder_name, user=request.user).todo_list.all()
    except TodoFolders.DoesNotExist:
        return redirect('home')

    if "uncompleted" in request.GET:
        todo_list = todo_list.filter(completed=False)
    elif 'completed' in request.GET:
        todo_list = todo_list.filter(completed=True)
    todo_folders = TodoFolders.objects.filter(user=request.user)
    context = {'todo_list': todo_list,
               "todo_folders": todo_folders, "folder_name": folder_name}
    return render(request, 'core/folder.html', context)


@logout_required
def log_in(request):
    form = CustomLoginForm()
    reg_form = RegisterForm()

    if request.method == "POST":
        if "password_rep" in request.POST:
            formR = RegisterForm(data=request.POST)
            if formR.is_valid():
                password = formR.cleaned_data.get('password')
                password1 = formR.cleaned_data.get('password_rep')
                if password == password1:

                    user = formR.save(commit=False)
                    user.password = make_password(password)
                    user.save()
                    login(request, user,
                          backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('home')
                else:
                    context = {'form': form, "reg_form": reg_form,
                               'reg_errors': formR.errors.as_text()}
                    return render(request, 'core/login.html', context)
        else:
            formL = CustomLoginForm(request, data=request.POST)
            if formL.is_valid():
                username = formL.cleaned_data.get('username')
                password = formL.cleaned_data.get('password')
                user = authenticate(
                    request, username=username, password=password)
                if user:
                    login(request, user)
                    return redirect('home')
                else:  # if user with username or email exists, but wrong password
                    login_errors = "Wrong username or password."
                    context = {'form': form, "reg_form": reg_form,
                               'login_errors': login_errors}
                    return render(request, 'core/login.html', context)
            else:  # if email or username wrong
                login_errors = "Wrong username or password."

                context = {'form': form, "reg_form": reg_form,
                           'login_errors': login_errors}
                return render(request, 'core/login.html', context)

    context = {'form': form, "reg_form": reg_form}
    return render(request, 'core/login.html', context)


def log_out(request):
    logout(request)
    return redirect('home')


def create_example_user(request):
    try:
        new_user = CustomUser(email="example@gmail.com",
                              username="Useriko", password=make_password("qwerty123"))
        new_user.save()
    except Exception:
        pass
    return redirect('home')
