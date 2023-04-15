from functools import wraps

from rest_framework.response import Response
from rest_framework import status

from schoolboxauth.models import User


def token_auth(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if not User.from_token(request):
            return Response({}, status.HTTP_401_UNAUTHORIZED)
        else:
            return function(request, *args, **kwargs)

    return wrap