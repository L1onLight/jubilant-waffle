import datetime

from django.db import models
from django.utils import timezone
from pytils.translit import slugify
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from user.models import CustomUser

WEEK = ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")


class FrequencyError(Exception):
    pass


# Create your models here.
class TodoCycle(models.Model):
    FREQUENCY_TYPES = (("daily", "DAILY"), ("weekly", "WEEKLY"), ("monthly", "MONTHLY"))

    todo_id = models.IntegerField(unique=True)
    start_date = models.DateField()

    frequency_type = models.CharField(choices=FREQUENCY_TYPES, max_length=20)
    frequency = models.JSONField(null=True, max_length=120)
    end_date = models.DateField(null=True)

    next_notification = models.DateField()

    def __str__(self):
        return f"<TodoCycle: {self.id}>"

    @staticmethod
    def get_next_notification_date(frequency_type: str, start_date: datetime.date, days: list | str = None):
        if days and type(days) is str:
            days = list(days)
        next_notification = start_date
        current_day = start_date.weekday() + 1
        if frequency_type == "daily":
            next_notification += timedelta(days=1)
        elif frequency_type == "month":
            next_notification += relativedelta(months=1)
        elif frequency_type == "weekly":
            if len(days) == 1 and days[0] == current_day:
                next_notification += timedelta(days=7)
            if max(days) > current_day:
                day = [day for day in days if day > current_day][0]
                for i in range(1, 8):
                    check = ((next_notification + timedelta(days=i)).weekday()) + 1
                    if check == day:
                        next_notification += timedelta(days=i)
                        break
            elif min(days) < current_day:
                for i in range(1, 8):
                    if (next_notification + timedelta(days=i)).weekday() + 1 == min(days):
                        next_notification += timedelta(days=i)
                        break
        else:
            raise Exception("Wrong frequency type")
        return next_notification

    @classmethod
    def validate_and_save(cls, todo_id: int, start_date: datetime.date,
                          frequency_type: str,
                          frequency: list = None,
                          end_date: datetime.date = None):
        if frequency_type == "daily" or frequency_type == "month":
            frequency = None

        next_notification = cls.get_next_notification_date(frequency_type=frequency_type, start_date=start_date,
                                                           days=frequency)
        if frequency:
            frequency = str(frequency)
        cycle = cls(todo_id=todo_id, start_date=start_date, end_date=end_date, frequency_type=frequency_type,
                    frequency=frequency,
                    next_notification=next_notification)
        cycle.save()
        return cycle


class Todo(models.Model):
    """For creating requires user and title.
    On default, completed=False. Updated and created auto.
    Until unnecessary."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    until = models.DateField(null=True, blank=True)
    cycle = models.ForeignKey(TodoCycle, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['-is_completed', '-updated_at', '-created_at']

    def __str__(self):
        return self.title

    def until_date(self):
        return self.until.strftime("%B %d, %Y")

    def until_time(self):
        return self.until.strftime("%H:%M")

    def change_state(self, state: bool):
        if state is True:
            self.completed_at = timezone.now()
            self.is_completed = True
        else:
            self.completed_at = None
            self.is_completed = False
        self.save()
        return self


class TodoFolders(models.Model):
    """Required user and folder_title fields. todo_list can be added after model created.
    user: User
    folder_title: str(50)
    todo_list: ManyToMany=> To-do"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    folder_title = models.CharField(max_length=50)
    todo_list = models.ManyToManyField(Todo, blank=True)

    slug = models.SlugField(blank=True, max_length=255)

    class Meta:
        unique_together = ("user", "folder_title"), ("user", "slug")

    def __str__(self):
        return self.folder_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.folder_title)
        super(TodoFolders, self).save(*args, **kwargs)
