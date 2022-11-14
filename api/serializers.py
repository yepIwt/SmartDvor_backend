from rest_framework import serializers
from api.models import User, Post

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
