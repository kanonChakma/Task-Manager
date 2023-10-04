from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if len(username) < 6:
            raise forms.ValidationError(
                "Username should be at least 6 characters long."
            )
        if username == "admin":
            raise forms.ValidationError("Username cannot be 'admin'.")
        return username

    def clean_password1(self):
        password1 = self.cleaned_data["password1"]
        if len(password1) < 8:
            raise forms.ValidationError(
                "Password should be at least 8 characters long."
            )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
