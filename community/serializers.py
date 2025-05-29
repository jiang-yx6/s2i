from rest_framework import serializers
from .models import UserPost, Tags, Image

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_id', 'image', 'created_at']
        read_only_fields = ['image_id', 'created_at']

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['tag_id', 'tag_name']

class UserPostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField()
    tags = TagsSerializer(many=True, read_only=True)
    
    class Meta:
        model = UserPost
        fields = ['post_id', 'title', 'description', 'images', 
                 'browse_count', 'like_count', 'created_at', 
                 'updated_at', 'author', 'tags']
        read_only_fields = ['post_id', 'browse_count', 'like_count', 
                           'created_at', 'updated_at', 'author'] 