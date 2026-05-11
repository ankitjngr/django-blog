from rest_framework import serializers
from .models import Post, Comment, Like, UserProfile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = ['id', 'username']


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['author', 'post']



class likeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like 
        fields = '__all__'
        read_only_fields = ['user', 'post']





class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    comments = CommentSerializer(
        read_only= True,
          many=True
          )

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['author']






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username', 
            'password', 
            'email',
            'first_name',
            'last_name',
            ]

        extra_kwargs = {
            'password': {'write_only': True}

        }

    def create(self, validated_data):
        print("Creating user with data: with create method")
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email',),
            first_name=validated_data.get('first_name', ),
            last_name=validated_data.get('last_name'),


        )
        return user
    
class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user', 'created_at']