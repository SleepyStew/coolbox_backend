from rest_framework.test import APIClient

from schoolboxauth.backend import hash_token
from schoolboxauth.models import User, Token


def authenticated_test_client():
    client = APIClient()
    token = "test_token"
    user = User(
        id=1,
        name="Test User",
    )
    user.save()
    token_object = Token(token=hash_token(token), user=user, valid=True)
    token_object.save()
    client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
    client.user = user
    return client
