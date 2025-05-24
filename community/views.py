from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserPost, Tags
from .serializers import UserPostSerializer, TagsSerializer

# Create your views here.
class CommunityPostCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = UserPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SavePost(APIView):
    pass

class CommunityList(APIView):
    def get(self, request):
        posts = UserPost.objects.all()
        serializer = UserPostSerializer(posts, many=True)
        return Response(serializer.data)

class CommunityDetail(APIView):
    def get(self, request, pk):
        post = get_object_or_404(UserPost, pk=pk)
        post.browse_count += 1
        post.save()
        serializer = UserPostSerializer(post)
        return Response(serializer.data)

class CommunityUpdate(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        post = get_object_or_404(UserPost, pk=pk)
        if post.author != request.user:
            return Response({"error": "您没有权限修改此帖子"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserPostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommunityDelete(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        post = get_object_or_404(UserPost, pk=pk)
        if post.author != request.user:
            return Response({"error": "您没有权限删除此帖子"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class CommunityLike(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(UserPost, pk=pk)
        post.like_count += 1
        post.save()
        return Response({"message": "点赞成功", "like_count": post.like_count})


