from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import TemplateView
from rest_framework import filters, generics, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import (
    SAFE_METHODS,
    BasePermission,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .forms import TaskFilterForm, TaskForm, TaskUpdateForm
from .models import Task, TaskPhoto
from .serailizers import TaskSerializer


# TEMPLATE VIEW
class TasksView(TemplateView):
    model = Task
    template_name = "tasks/home.html"
    context_object_name = "tasks"
    paginate_by = 10

    def get_queryset(self):
        queryset = Task.objects.all()

        # Filter by title
        title = self.request.GET.get("title")
        if title:
            queryset = queryset.filter(title__icontains=title)

        # Filter by creation date

        # Filter by due date
        due_date = self.request.GET.get("due_date")
        if due_date:
            queryset = queryset.filter(due_date__date=due_date)

        # Filter by priority
        priority = self.request.GET.get("priority")
        if priority:
            queryset = queryset.filter(priority=priority)

        # Filter by completion status
        is_complete = self.request.GET.get("is_complete")
        if is_complete == "on":
            queryset = queryset.filter(is_complete=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filter_form"] = TaskFilterForm(self.request.GET)
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
        else:
            messages.error(
                request, "There Was An Error Logging In, Please Try Again..."
            )

        return redirect("home")


class TaskDetailsView(generic.DetailView):
    model = Task
    template_name = "tasks/task_details.html"
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.object

        photos = TaskPhoto.objects.filter(task=task)
        context["photos"] = photos

        return context


class TaskCreateView(generic.CreateView):
    form_class = TaskForm
    template_name = "tasks/task_create.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "The task was created successfully.")
        self.object = form.save()

        images = self.request.FILES.getlist("images")
        for image in images:
            TaskPhoto.objects.create(task=self.object, photo=image)

        return super(TaskCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse("task_list")


class TaskDeleteView(generic.DeleteView):
    model = Task
    template_name = "tasks/task_delete.html"
    context_object_name = "task"
    success_url = reverse_lazy("task_list")


class TaskImageDeleteView(generic.DeleteView):
    model = TaskPhoto
    template_name = "tasks/task_image_delete.html"
    context_object_name = "taskphoto"

    def get_success_url(self):
        return reverse_lazy("task_update", kwargs={"pk": self.object.task.pk})


class TaskUpdateView(generic.UpdateView):
    model = Task
    form_class = TaskUpdateForm
    template_name = "tasks/task_update.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        # Handle file uploads (TaskImageModel creation) separately
        images = self.request.FILES.getlist("images")
        for image in images:
            TaskPhoto.objects.create(task=self.object, image=image)

        return response

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     form = self.get_form()
    #     if form.is_valid():
    #         form.instance.user = self.request.user
    #         response = super().form_valid(form)
    #     else:
    #         response = self.form_invalid(form)

    #     # Handle file uploads (TaskPhoto creation) separately
    #     images = self.request.FILES.getlist("images")
    #     for image in images:
    #         TaskPhoto.objects.create(task=self.object, photo=image)

    #     return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()

        formatted_due_date = task.due_date.strftime("%Y-%m-%d")
        context["formatted_due_date"] = formatted_due_date

        photos = TaskPhoto.objects.filter(task=task)
        context["photos"] = photos

        return context

    def get_success_url(self):
        return reverse("task_list")


# API FOR ALL
class CreateTaskViewAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request: Request, format=None) -> Response:
        task_serializer = TaskSerializer(data=request.data)
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(
                data={
                    "message": "Task created successfully",
                    "task": task_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data={"message": task_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


class TaskDetailViewAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request: Request, task_id) -> Response:
        try:
            task = Task.objects.get(pk=task_id)
            task_serializer = TaskSerializer(instance=task)
            return Response(data=task_serializer, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response(
                data={"message": "Task does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def put(self, request: Request, task_id) -> Response:
        try:
            task = Task.objects.get(pk=task_id)
            if task.user.id != request.user.id:
                return Response(
                    data={"message": "You are unauthorized to update!!!!"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            task_serializer = TaskSerializer(
                instance=task, data=request.data, partial=True
            )
            if task_serializer.is_valid(raise_exception=True):
                task_serializer.save()
                return Response(
                    data={
                        "message": "Task updated successfully!!!",
                        "task": task_serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )

        except Task.DoesNotExist:
            return Response(
                data={"message": "Task does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request: Request, task_id) -> Response:
        try:
            task = Task.objects.get(pk=task_id)
            if task.user.id != request.user.id:
                return Response(
                    data={"message": "You are unauthorized to delete!!!"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            task.delete()
            return Response(
                data={"message": "Task deleted successfully!!!"},
                status=status.HTTP_200_OK,
            )

        except Task.DoesNotExist:
            return Response(
                data={"message": "Task does not exist"},
                status=status.HTTP_404_NOT_FOUND,
            )
