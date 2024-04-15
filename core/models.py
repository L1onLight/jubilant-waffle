import datetime

from django.db import models
from django.utils import timezone
from pytils.translit import slugify

from user.models import CustomUser


# Create your models here.


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
