from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from . import serializers
from api.models import User

# Create your views here. Okay.


def welcome(request) -> HttpResponse:
    return HttpResponse(f"<h1>Hello, {request.user}!</h1>")


class RegisterView(APIView):
    def post(self, request) -> Response:
        serializer = serializers.UserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)