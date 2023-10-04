from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, email, username, first_name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must be assigned to is_superuser=True.")

        return self.create_user(email, username, first_name, password, **other_fields)

    def create_user(self, email, username, first_name, password, **other_fields):
        if not email:
            raise ValueError(_("You must provide an email address"))

        email = self.normalize_email(email)
        user = self.model(
            email=email, user_name=username, first_name=first_name, **other_fields
        )
        user.set_password(password)
        user.save()
        return user


def upload_to_path(instance, filename):
    user_id: str = instance.id
    return f"{settings.PROFILE_IMAGE_DIR_NAME}/{user_id}-{filename}"


class NewUser(AbstractBaseUser, PermissionsMixin):
    GENDER = [
        ("Male", _("Male")),
        ("Female", _("Female")),
    ]
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    birth_date = models.DateField(auto_now_add=False, null=True, blank=True)
    about = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    gender = models.CharField(choices=GENDER, max_length=6, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)

    profile_image = models.ImageField(
        upload_to=upload_to_path, max_length=300, null=True, blank=True
    )

    objects = CustomAccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name"]

    def __str__(self):
        return self.username
