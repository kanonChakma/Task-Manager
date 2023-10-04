class TaskUpdateView(generic.UpdateView):
    model = Task
    template_name = "tasks/task_update.html"
    fields = ["title", "description", "is_complete", "due_date", "priority"]
    success_url = reverse_lazy("task_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()

        formatted_due_date = task.due_date.strftime("%Y-%m-%d")
        context["formatted_due_date"] = formatted_due_date

        photos = TaskPhoto.objects.filter(task=task)
        context["photos"] = photos

        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        images = self.request.FILES.getlist("images")
        for image in images:
            TaskPhoto.objects.create(task=self.object, image=image)

        return response