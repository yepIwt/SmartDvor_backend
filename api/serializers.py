from rest_framework import serializers
from api.models import User, Post, PostComment, Service

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'address', 'sex', 'birthday', 'date_joined']
        extra_kwargs = {
            'password': {'write_only': True},
            'birthday': {'required': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['post_title', 'post_text', 'pub_date', 'post_author']

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ["post", "comment_text", "comment_author", "pub_date"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ["customer", "service_type", "customer_comment", "pub_date", "status", "status_comment"]

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance