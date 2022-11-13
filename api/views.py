import datetime
import jwt
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


class LoginView(APIView):
    def post(self, request):
        if not request.data.get("username") or not request.data.get("password"):
            raise AuthenticationFailed({
                "username": "username",
                "password": "password"
            })

        username = request.data["username"]
        password = request.data["password"]

        user = User.objects.filter(username = username).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes = 60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "secret", algorithm = "HS256")

        response = Response()

        response.set_cookie(key = "jwt", value = token, httponly = True)
        response.data = {
            "jwt": token
        }
        return response
