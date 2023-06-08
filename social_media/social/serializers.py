from rest_framework import serializers
from .models import *
from rest_framework.fields import CurrentUserDefault
from datetime import datetime

class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = ['user', 'description', 'image']

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=True)
    class Meta:
        model = Profile
        fields = ['user', 'follows', 'date_modified', 'intro']


class UserListSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','profile']


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password']
        extra_kwargs = {'password': {'write_only': True}}


class PostListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    created_at = serializers.DateTimeField(format="%b. %d, %Y, %I:%M %p")
    class Meta:
        model = Post
        fields = ['user', 'description', 'image', 'thumbnail', 'created_at']



class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ('username', 'room', 'message', 'timestamp')
