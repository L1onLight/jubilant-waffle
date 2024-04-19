from django.utils import timezone
from rest_framework import serializers
from core.models import Todo, TodoFolders, TodoCycle


class CreateCycleSerializer(serializers.ModelSerializer):
    frequency_type = serializers.CharField()
    frequency = serializers.JSONField(required=False)

    class Meta:
        model = TodoCycle
        fields = ["frequency_type", "frequency"]


class CycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoCycle
        fields = [
            "frequency_type",
            "frequency",
            "next_notification"]


class TodoCreateSerializer(serializers.ModelSerializer):
    # Slug required to add to-do directly to folder
    slug = serializers.SlugField(required=False)
    cycle = CreateCycleSerializer(required=False)

    class Meta:
        model = Todo
        fields = ["title", "until", "slug", "cycle"]

    def create(self, validated_data):
        user = self.context["request"].user
        cycle = validated_data.pop("cycle", None)
        instance = Todo(user_id=user.id, **validated_data)
        instance.save()

        if cycle:
            today = timezone.now().date()
            cycle = TodoCycle.validate_and_save(todo_id=instance.id, start_date=today,
                                                end_date=validated_data.get("until"),
                                                **dict(cycle))
            instance.cycle = cycle
            instance.save()
        return instance


class QueryFilterSerializer(serializers.Serializer):
    query = serializers.CharField(required=False)


class TodoRetrieveSerializer(serializers.ModelSerializer):
    cycle = CycleSerializer()

    class Meta:
        model = Todo
        fields = ["id", "title", "is_completed", "completed_at", "cycle", "until", "created_at", "updated_at"]


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
