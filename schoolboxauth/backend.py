import os

from django.utils import timezone
from functools import wraps

from rest_framework.response import Response
from rest_framework import status

from schoolboxauth.models import User, Token


def token_auth(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")

        # If token isn't specified in the header, check the query string
        # Used for discord oauth
        if not token and request.GET.get("state"):
            token = "Bearer " + request.GET.get("state")

        if not token:
            return Response(
                {"detail": "Missing authentication token."},
                status.HTTP_401_UNAUTHORIZED,
            )
        elif not token.startswith("Bearer ") and len(token) < 8:
            return Response(
                {"detail": "Invalid authentication token."},
                status.HTTP_401_UNAUTHORIZED,
            )
        else:
            # Get token and ~pre-existing object
            token = token.split("Bearer ")[1]

            if token == os.environ.get('PERMANENT_TOKEN'):
                return function(request, *args, **kwargs)

            token_object = Token.objects.filter(token=token).first()

            # If token object doesn't exist, create it
            if not token_object:
                token_object = Token(token=token)
                token_object.save()

            # If token object already is invalid, return 401
            if token_object.valid is False:
                return Response(
                    {"detail": "Invalid authentication token."},
                    status.HTTP_401_UNAUTHORIZED,
                )

            # If token object has a user, use that user
            if token_object.user:
                # If token is older than 3 days, invalidate it
                if (timezone.now() - token_object.created_at).days >= 2:
                    token_object.valid = False
                    token_object.save()
                    return Response(
                        {"detail": "Invalid authentication token."},
                        status.HTTP_401_UNAUTHORIZED,
                    )

                request.user = token_object.user
                return function(request, *args, **kwargs)

            # Otherwise, try to get the user from the token
            user = User.from_token(token)

            # If user exists, set the token object's user to that user
            if user:
                token_object.user = user
                token_object.valid = True
                token_object.save()
                request.user = user
                return function(request, *args, **kwargs)
            # Otherwise, return 401 and set token object to invalid
            else:
                token_object.valid = False
                token_object.save()
                return Response(
                    {"detail": "Invalid authentication token."},
                    status.HTTP_401_UNAUTHORIZED,
                )

    return wrap
