from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "due_date", "priority"]


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "due_date",
            "priority",
            "is_complete",
        ]


class TaskFilterForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "due_date", "priority", "is_complete"]
