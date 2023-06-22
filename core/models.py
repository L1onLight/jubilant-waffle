from django.db import models
from user.models import CustomUser
# Create your models here.


class Todo(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    completed = models.BooleanField(default=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    completedTime = models.DateTimeField()
    until = models.DateTimeField()

    def __str__(self):
        return self.title
