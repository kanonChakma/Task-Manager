from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import LoginForm, MyUserCreationForm, UserCreationForm


# Home page
def index(request):
    return render(request, "accounts/index.html")


# signup page
def user_signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})


# login page
def user_login(request):
    if request.user.is_authenticated:
        return redirect("/api/tasks/")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect("/api/tasks/")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


# logout page
def user_logout(request):
    logout(request)
    return redirect("login")


def regitsterPage(request):
    if request.user.is_authenticated:
        return redirect("/api/tasks/")

    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect("/api/tasks/")
        else:
            print(form.errors)

    else:
        form = MyUserCreationForm()

    return render(request, "accounts/signup.html", {"page": "register", "form": form})
