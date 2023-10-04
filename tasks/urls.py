from django.urls import path

from .views import (
    TaskCreateView,
    TaskDeleteView,
    TaskDetailsView,
    TaskImageDeleteView,
    TasksView,
    TaskUpdateView,
)

urlpatterns = [
    path("", TasksView.as_view(), name="task_list"),
    path("detail/<int:pk>/", TaskDetailsView.as_view(), name="task_details"),
    path("delete/<int:pk>/", TaskDeleteView.as_view(), name="task_delete"),
    path(
        "image-delete/<int:pk>/",
        TaskImageDeleteView.as_view(),
        name="task_image_delete",
    ),
    path("update/<int:pk>/", TaskUpdateView.as_view(), name="task_update"),
    path("create/", TaskCreateView.as_view(), name="task_create"),
]
