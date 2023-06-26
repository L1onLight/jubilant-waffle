from django.db import models
from user.models import CustomUser


# Create your models here.


class Todo(models.Model):
    """For creating requires user and title.
    On default, completed=False. Updated and created auto.
    Until unrequired, but can be added."""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    completedTime = models.DateTimeField(null=True, blank=True)
    until = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-completed', '-updated', '-created']

    def __str__(self):
        return self.title

    def until_date(self):
        return self.until.strftime("%B %d, %Y")

    def until_time(self):
        return self.until.strftime("%H:%M")


class TodoFolders(models.Model):
    """Required user and folder_title fields. todo_list can be added after model created.\n
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)\n
    folder_title = models.CharField(max_length=50)\n
    todo_list = models.ManyToManyField(Todo, blank=True)"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    folder_title = models.CharField(max_length=50)
    todo_list = models.ManyToManyField(Todo, blank=True)

    class Meta:
        unique_together = ("user", "folder_title")

    def __str__(self):
        return self.folder_title
