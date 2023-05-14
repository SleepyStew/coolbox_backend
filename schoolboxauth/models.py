import json

import requests
import rest_framework_simplejwt.exceptions
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models


# Create your models here.
class Token(models.Model):
    token = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    valid = models.BooleanField(default=None, null=True)
    user = models.ForeignKey("User", on_delete=models.CASCADE, null=True)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=128, unique=True)
    year = models.CharField(max_length=2, null=True)
    role = models.CharField(max_length=64, default="student")
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
            role = json.loads(
                response.text.split("schoolboxUser.role           = ")[1].split(";")[0]
            )["type"]

            user = User.objects.filter(id=user_id).first()

            if not user:
                user = User(
                    id=user_id,
                    name=response.text.split(',"fullName":"')[1].split('"')[0],
                    role=role,
                )
                if role == "student":
                    user.year = (
                        response.text.split('schoolboxUser.year           = "')[
                            1
                        ].split('"')[0],
                    )
                user.save()
            else:
                user.name = response.text.split(',"fullName":"')[1].split('"')[0]
                user.role = role
                if role == "student":
                    user.year = response.text.split('schoolboxUser.year           = "')[
                        1
                    ].split('"')[0]
                user.save()

            return user

        except rest_framework_simplejwt.exceptions.TokenBackendError:
            return False
