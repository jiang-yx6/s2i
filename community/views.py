from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import F
from .models import UserPost, Tags, Image, Comment
from .serializers import UserPostSerializer, CommentSerializer
from datetime import datetime

# Create your views here.
# 创建新帖子
class CommunityPostCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request):
        try:
            # 获取文本数据
            post_data = {
                'title': request.data.get('title'),
                'description': request.data.get('description')
            }
            print("post_data: ",post_data)
            
            # 验证必填字段
            if not post_data['title'] or not post_data['description']:
                return Response({
                    'error': '标题和内容为必填项'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # 创建帖子
            post_serializer = UserPostSerializer(data=post_data)

            if post_serializer.is_valid():
                post = post_serializer.save(author=request.user)
                print("post: ",post)
                
                # 处理图片上传（如果有的话）
                images = request.FILES.getlist('images', [])
                if images:
                    print("images: ",images)
                    for image_file in images:
                        try:
                            # 直接创建与帖子关联的图片
                            Image.objects.create(
                                image=image_file,
                                post=post
                            )
                            print("图片上传成功",image_file)
                        except Exception as e:
                            print(f"图片上传失败: {str(e)}")
                            continue
                
                # 重新序列化帖子（包含新上传的图片）
                response_serializer = UserPostSerializer(post)
                return Response({
                    'message': '帖子创建成功',
                    'data': response_serializer.data,
                    'success': True
                }, status=status.HTTP_201_CREATED)
            
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            return Response({
                'error': f'创建帖子失败: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 保存帖子
class SavePost(APIView):
    pass

# 获取所有帖子
class CommunityList(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        posts = UserPost.objects.all()
        serializer = UserPostSerializer(posts, many=True)
        
        # 如果用户已登录，添加是否点赞的信息
        if request.user.is_authenticated:
            data = serializer.data
            for post in data:
                post['is_liked'] = UserPost.objects.get(
                    post_id=post['post_id']
                ).like_users.filter(id=request.user.id).exists()
            return Response(data)
        
        return Response(serializer.data)

# 获取单个用户帖子
class CommunityListByUser(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        posts = UserPost.objects.filter(author=request.user)
        serializer = UserPostSerializer(posts, many=True)
        return Response(serializer.data)

# 获取单个帖子所有信息
class CommunityDetail(APIView):
    permission_classes = [AllowAny]
    def get(self, request, post_id):
        post = get_object_or_404(UserPost, post_id=post_id)
        post.browse_count += 1
        post.save()
        serializer = UserPostSerializer(post)
        comments = Comment.objects.filter(post=post)
        comment_serializer = CommentSerializer(comments, many=True)
        print("comments: ",comment_serializer.data)
        print("serializer: ",serializer.data)
        return Response({
            'post': serializer.data,
            'comments': comment_serializer.data
        })

# 更新帖子
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

# 删除帖子
class CommunityDelete(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        post = get_object_or_404(UserPost, pk=pk)
        if post.author != request.user:
            return Response({"error": "您没有权限删除此帖子"}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 点赞帖子
class CommunityLike(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, post_id):
        post = get_object_or_404(UserPost, post_id=post_id)
        like_type = request.data.get('like_type')
        if like_type == 'like':
            post.like_users.add(request.user)
            post.like_count = F('like_count') + 1
            print("点赞成功")
        elif like_type == 'unlike':
            post.like_users.remove(request.user)
            post.like_count = F('like_count') - 1
            print("取消点赞成功")
        post.save()
        # 重新获取更新后的帖子对象
        post.refresh_from_db()
        return Response({"message": "操作成功", "like_count": post.like_count})

    # 获取单用户喜欢的所有帖子
    def get(self, request, post_id):
        posts = UserPost.objects.filter(like_users=request.user)
        serializer = UserPostSerializer(posts, many=True)
        return Response(serializer.data)

# 创建评论
class CommentCreate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, post_id):
        post = get_object_or_404(UserPost, post_id=post_id)
        comment = Comment.objects.create(
            content=request.data.get('content'),
            post=post,
            author=request.user
        )
        comment_serializer = CommentSerializer(comment) 
        post.comment_count += 1
        post.save()
        print("comment_serializer: ",comment_serializer.data)
        return Response(comment_serializer.data)
