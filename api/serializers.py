from rest_framework import serializers
from core.models import Todo, TodoFolders


class TodoCreateSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)

    class Meta:
        model = Todo
        fields = ["title", "until", "slug"]

    def create(self, validated_data):
        user = self.context["request"].user
        return Todo.objects.create(user_id=user.id, **validated_data)


class QueryFilterSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)


class TodoRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "is_completed", "completed_at", "until", "created_at", "updated_at"]


class TodoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["title", "until"]


class TodoChangeStateSerializer(serializers.Serializer):
    state = serializers.BooleanField()


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoFolders
        fields = ("id", "folder_title")


class FolderRetrieveSerializer(serializers.ModelSerializer):
    todo_list = TodoRetrieveSerializer(many=True)

    class Meta:
        model = TodoFolders
        fields = ("id", "folder_title", "slug", "todo_list")


class AddToFolderSerializer(serializers.Serializer):
    folder_id = serializers.IntegerField()
