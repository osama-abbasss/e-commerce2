from rest_framework import serializers
from blog.models import Post


class PostSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField('get_username_from_user')
    #image = serializers.SerializerMethodField('validate_image_url')
    class Meta:
        model = Post
        fields = ['id', 'username', 'title', 'content',
                  'description', 'img', 'slug', 'created_at', 'active']

    def get_username_from_user(self, Post):
        username = Post.user.username
        return username

"""
    def validate_image_url(self, Post):
        image = Post.img
        new_url = image.url
        if '?' in new_url:
            new_url = image.url[:image.url.rfind('?')]
        return new_url

"""


class UpdatePostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = [ 'title', 'content','description', 'img', 'active']
