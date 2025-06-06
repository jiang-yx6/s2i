from rest_framework import serializers
from .models import UserPost, Tags, Image, Comment
from exts.format_time import format_time_ago
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
    is_liked = serializers.BooleanField(read_only=True, required=False)


    def get_created_at(self, obj):
        return format_time_ago(obj.created_at)
    
    
    class Meta:
        model = UserPost
        fields = ['post_id', 'title', 'description', 'images', 
                 'browse_count', 'like_count', 'created_at', 
                 'updated_at', 'author', 'tags', 'comment_count', 'is_liked']
        read_only_fields = ['post_id', 'browse_count', 'like_count', 
                           'created_at', 'updated_at', 'author', 'comment_count'] 

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment_id', 'content', 'created_at', 'post', 'author', 'like_count']
        read_only_fields = ['comment_id', 'created_at', 'post', 'author', 'like_count']
