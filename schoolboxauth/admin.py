from django.contrib import admin

from schoolboxauth.models import User, Token

# Register your models here.

admin.site.register(User)
admin.site.register(Token)
