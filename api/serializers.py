from core.models import Todo, TodoFolders
from rest_framework import serializers
from user.models import CustomUser


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoFolders
        # fields = '__all__'
        fields = ['id', 'folder_title', 'todo_list']
