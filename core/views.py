import asyncio

from django.shortcuts import render, get_object_or_404, redirect
from user.forms import RegisterForm, CustomLoginForm
from .models import Todo, TodoFolders
from django.contrib.auth import logout, get_user_model
from .decorators import *
from django.contrib import messages
from .models import CustomUser
from django.http import QueryDict
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from notifications.models import PasswordRestore
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import auth
import random
from notifications.views import send_password_restore_mail
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
def log_in(request, fool=None):
    form = CustomLoginForm()
    reg_form = RegisterForm()

    if request.method == "POST":
        if "password_rep" in request.POST:
            formR = RegisterForm(data=request.POST)
            if formR.is_valid():
                password = formR.cleaned_data.get('password')
                password1 = formR.cleaned_data.get('password_rep')
                if password == password1:
                    user = get_user_model().objects.create_user(email=formR.data.get("email"), password=password)
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


def restore_mail(request):
    if request.method == 'POST' and request.POST.get('restoreCode'):
        r_email = request.POST.get('restoreEmail')
        r_code = request.POST.get('restoreCode')
        r_password = request.POST.get('restorePassword')
        try:
            pr = PasswordRestore.objects.get(user__email=r_email)
            current_datetime = timezone.now()
            model_datetime = pr.created_or_changed
            if current_datetime > model_datetime + timedelta(minutes=1):
                pr.delete()
                messages.error(request, 'Code expired.')
            else:
                if r_code == str(pr.restoreCode):
                    user = CustomUser.objects.get(email=r_email)
                    user.password = make_password(r_password)
                    user.save()
                    auth.login(request, user=user, backend='django.contrib.auth.backends.ModelBackend')
                    return redirect('home')
                else:
                    messages.error(request, 'Wrong code.')
        except PasswordRestore.DoesNotExist:
            messages.error(request, 'Wrong code.')
            pass

    if request.method == 'POST' and '?code' not in request.build_absolute_uri():
        email_ = request.POST.get('email')

        try:
            user = CustomUser.objects.get(email=email_)
            code = random.randrange(1000000, 10000000)

            try:
                pr = PasswordRestore.objects.get(user=user)
                pr.restoreCode = code
                pr.save()
            except Exception as e:
                # pr = PasswordRestore.objects.create(user=user, restoreCode=code)
                pr = PasswordRestore(user=user, restoreCode=code)
                pr.save()
            # pr, created = PasswordRestore.objects.get_or_create(user=user)
            # pr.restoreCode = code
            # pr.save()
            print(f"Code: {code}")
            send_password_restore_mail(receiver_email=email_, code=code, url=request.build_absolute_uri('?code'))

            # p_restore(email_, code)
            messages.success(request, 'Check your email.')

        except CustomUser.DoesNotExist:
            # Here you can change error message to check your email if
            # you want to hide information about email from user.
            messages.error(request, 'User does not exist.')
    return render(request, 'core/password_restore.html')
