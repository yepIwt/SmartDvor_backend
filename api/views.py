import datetime
import jwt
import rest_framework.exceptions
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, ValidationError

from . import serializers
from api.models import User, Post, Service
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
    def post(self, request) -> Response:
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
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days = 60),
            "iat": datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "secret", algorithm = "HS256")

        response = Response()

        response.set_cookie(key = "jwt", value = token, httponly = True)
        response.data = {
            "jwt": token
        }
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()

        response.delete_cookie("jwt")
        response.data = {
            "message": "success"
        }
        return response

class UserView(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms = ["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        user = User.objects.filter(id = payload["id"]).first()
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)


class UserGetView(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms = ["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        if not request.data.get("id"):
            return Response(
                {"id": "required"}
            )

        user = User.objects.get(id = request.data["id"])
        serializer = serializers.UserSerializer(user)
        return Response(serializer.data)

class UserListView(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        users = User.objects.all()
        serializer = serializers.UserSerializer(users, many=True)  # TODO: restrict access to personal data
        return Response(serializer.data)

class PostListView(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        posts = Post.objects.all()
        serializer = serializers.PostSerializer(posts, many=True)
        return Response(serializer.data)

class PostCreateView(APIView):
    def post(self, request) -> Response:
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        request.data._mutable = True
        request.data.setdefault("post_author", payload["id"])

        serializer = serializers.PostSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(serializer.data)


class PostCommentListView(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        if not request.data.get("post_id"):
            raise ValidationError("'post_id' required")

        post = Post.objects.get(id = request.data["post_id"])  # TODO: index out of the range!

        comments = post.postcomment_set.order_by('-id')
        serializer = serializers.PostCommentSerializer(comments, many = True)
        return Response(serializer.data)

class PostCommentLeaveView(APIView):
    def post(self, request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        if not request.data.get("post_id"):
            return Response({"post_id" : "required"})

        request.data._mutable = True
        request.data.setdefault("comment_author", payload["id"])
        request.data.setdefault("post", request.data["post_id"])  # TODO: index out of the range!

        serializer = serializers.PostCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ServiceListView(APIView):  # TODO: Only superuser can view this
    def get(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        people_requests = Service.objects.all()
        serializer = serializers.ServiceSerializer(people_requests, many = True)
        return Response(serializer.data)

class ServiceRequestView(APIView):
    def post(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        request.data._mutable = True
        request.data.setdefault("customer", payload["id"])

        serializer = serializers.ServiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ServiceCustomerListView(APIView):
    def get(self, request):

        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Unauthenticated!")

        customer = User.objects.get(id = payload["id"])
        requests = customer.service_set.order_by('-id')
        serializer = serializers.ServiceSerializer(requests, many=True)
        return Response(serializer.data)