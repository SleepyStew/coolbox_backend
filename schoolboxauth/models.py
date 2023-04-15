import rest_framework_simplejwt.exceptions
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework_simplejwt.backends import TokenBackend

from coolbox_backend import settings


# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=64, primary_key=True)
    cookie = models.CharField(max_length=64)
    name = models.CharField(max_length=128, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    required_fields = ["id", "cookie", "name"]

    USERNAME_FIELD = "name"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def from_token(request):
        try:
            return User.objects.get(id=TokenBackend(algorithm="HS256", signing_key=settings.SECRET_KEY).decode(request.META.get("HTTP_AUTHORIZATION"))['user_id'])
        except rest_framework_simplejwt.exceptions.TokenBackendError:
            return False
