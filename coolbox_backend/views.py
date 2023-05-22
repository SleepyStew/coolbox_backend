# Create your views here.
from rest_framework.views import APIView
from django.shortcuts import redirect


# Create your views here.
class IndexView(APIView):
    def get(self, request):
        return redirect("https://github.com/SleepyStew/coolbox_backend")
