import datetime

from django.conf import settings
from django.contrib.auth import get_user_model

from core.models import Todo, TodoFolders
import pytz

TIME_ZONE = pytz.timezone(settings.TIME_ZONE)
time_format = "%Y-%m-%d"


def format_time(datetime_time: datetime.datetime):
    return datetime_time.strftime(time_format)


def assert_time(json_time: str, datetime_time: datetime.datetime):
    time = datetime.datetime.fromisoformat(json_time).date()
    return time, datetime_time


def create_test_user(**kwargs):
    defaults = {
        "email": "test@example.com",
        "password": "testpass123",
    }
    defaults.update(kwargs)
    return get_user_model().objects.create_user(**defaults)


def create_test_todo(user, **kwargs):
    defaults = {
        "title": "TestTodo",
    }
    defaults.update(kwargs)

    return Todo.objects.create(user=user, **defaults)


def create_test_folder(user, **kwargs):
    defaults = {
        "user": user,
        "folder_title": "TestTodoFolder",
    }
    defaults.update(kwargs)

    return TodoFolders.objects.create(**defaults)
