from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user_profile_image = serializers.ImageField(
        source="user.profile_image", read_only=True
    )
    user_name = serializers.CharField(source="author.user_name", read_only=True)

    class Meta:
        fields = (
            "id",
            "title",
            "due_date",
            "priority",
            "is_complete",
            "created_at",
            "user",
            "user_profile_image",
            "user",
        )
        model = Task
