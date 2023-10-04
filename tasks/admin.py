from django.contrib import admin

from .models import Task, TaskPhoto


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "priority",
        "title",
        "description",
        "due_date",
        "is_complete",
        "user",
    ]
    ordering = ("priority",)


@admin.register(TaskPhoto)
class TaskPhotoAdmin(admin.ModelAdmin):
    list_display = ["id", "task"]
