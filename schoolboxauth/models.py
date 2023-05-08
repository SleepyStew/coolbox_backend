import requests
import rest_framework_simplejwt.exceptions
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from rest_framework_simplejwt.backends import TokenBackend

from coolbox_backend import settings


# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=512)
    valid = models.BooleanField(default=None, null=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "name"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    @staticmethod
    def from_token(token):
        try:
            response = requests.get(
                "https://schoolbox.donvale.vic.edu.au",
                cookies={
                    "PHPSESSID": f"{token}",
                },
            )

            if (
                "userNameInput.placeholder = 'Sample.User@donvale.vic.edu.au';"
                in response.text
            ):
                return False

            user_id = response.text.split('= {"id":')[1].split('"')[0][:-1]

            user = User.objects.filter(id=user_id).first()

            if not user:
                user_name = response.text.split(',"fullName":"')[1].split('"')[0]
                user = User(id=user_id, name=user_name)
                user.save()

            return user

        except rest_framework_simplejwt.exceptions.TokenBackendError:
            return False
