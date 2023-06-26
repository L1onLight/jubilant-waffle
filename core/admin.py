from django.contrib import admin
from .models import Todo, TodoFolders
# Register your models here.
admin.site.register(Todo)
admin.site.register(TodoFolders)
