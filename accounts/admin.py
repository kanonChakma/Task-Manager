from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.db import models
from django.forms import CharField, Textarea, TextInput

NewUser = get_user_model()


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = (
        "email",
        "username",
        "first_name",
    )
    list_filter = ("email", "username", "first_name", "is_active", "is_staff")
    ordering = ("-start_date",)
    list_display = ("email", "username", "first_name", "is_active", "is_staff")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "email",
                    "username",
                    "first_name",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Personal", {"fields": ("about",)}),
        ("Upload image", {"fields": ("profile_image",)}),
    )
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={"rows": 20, "cols": 60})},
    }
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "first_name",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                ),
            },
        ),
    )


admin.site.register(NewUser, UserAdminConfig)
