import hashlib
import os
import time
from functools import wraps

from django.contrib.auth.backends import BaseBackend
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from schoolboxauth.models import User, Token

ERROR_TOKEN_INVALID = "Invalid authentication token."
ERROR_TOKEN_MISSING = "Missing authentication token."
ERROR_NO_PERMISSION = "You do not have permission to perform this action."


def hash_token(token):
    m = hashlib.sha256()
    m.update(token.encode("utf-8"))
    return m.hexdigest()


def verify_token(function, request, internal=False, *args, **kwargs):
    token = request.META.get("HTTP_AUTHORIZATION")

    # If token isn't specified in the header, check the query string
    # Used for discord oauth
    if not token and request.GET.get("state"):
        token = "Bearer " + request.GET.get("state")

    if not token:
        return Response(
            {"detail": ERROR_TOKEN_MISSING},
            status.HTTP_401_UNAUTHORIZED,
        )

    elif not token.startswith("Bearer ") and len(token) < 8:
        return Response(
            {"detail": ERROR_TOKEN_INVALID},
            status.HTTP_401_UNAUTHORIZED,
        )
    else:
        # Get token and ~pre-existing object
        token = token.split("Bearer ")[1]

        if internal:
            if token == os.environ.get("PERMANENT_TOKEN"):
                return function(request, *args, **kwargs)

            return Response(
                {"detail": ERROR_NO_PERMISSION},
                status.HTTP_403_FORBIDDEN,
            )

        token_hash = hash_token(token)
        token_object = Token.objects.filter(token=token_hash).first()

        if token_object:
            # If token object already is invalid, return 401
            if token_object.valid is False:
                return Response(
                    {"detail": ERROR_TOKEN_INVALID},
                    status.HTTP_401_UNAUTHORIZED,
                )

            # If token object has a user, use that user
            if token_object.user:
                # If token is older than 24 hours, invalidate it
                if (timezone.now() - token_object.created_at).days >= 1:
                    token_object.valid = False
                    token_object.save()
                    return Response(
                        {"detail": ERROR_TOKEN_INVALID},
                        status.HTTP_401_UNAUTHORIZED,
                    )
                if token_object.user.name != "Test User":
                    print(f"User: {token_object.user.name}")
                request.user = token_object.user
                request.token = token
                return function(request, *args, **kwargs)

        else:
            # Otherwise, try to get the user from the token
            user = User.from_token(token)

            token_object = Token.objects.filter(token=token_hash).first()

            # If user exists, set the token object's user to that user
            # And token still doesn't exist
            if user:
                if user.name != "Test User":
                    print(f"User: {user.name}")
                if not token_object:
                    token_object = Token(token=token_hash, user=user, valid=True)
                    token_object.save()
                request.user = user
                request.token = token
                return function(request, *args, **kwargs)
            # Otherwise, return 401 and set token object to invalid
            else:
                token_object = Token(token=token_hash, valid=False)
                token_object.save()
                return Response(
                    {"detail": ERROR_TOKEN_INVALID},
                    status.HTTP_401_UNAUTHORIZED,
                )


def token_auth(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        return verify_token(function, request, *args, **kwargs)

    return wrap


def internal_auth(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        return verify_token(function, request, *args, **kwargs, internal=True)

    return wrap


def delete_old_tokens():
    while True:
        for token in Token.objects.all():
            if (timezone.now() - token.created_at).days >= 7:
                token.delete()
        time.sleep(1800)


def print_user(request):
    print(request)


class SchoolboxAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        user = User.from_token(username)
        password_valid = password == os.environ.get("ADMIN_PASSWORD")
        if not user or not password_valid:
            return None
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
