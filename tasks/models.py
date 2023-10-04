from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


def upload_to_path(instance, filename):
    return f"{settings.TASK_IMAGE_DIR_NAME}/{filename}"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    priority = models.CharField(
        max_length=10, choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")]
    )
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title


class TaskPhoto(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="photos")
    photo = models.ImageField(upload_to=upload_to_path, default="task.jpg")
