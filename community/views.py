from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import F
from .models import UserPost, Tags, Image
from .serializers import UserPostSerializer

# Create your views here.
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

class SavePost(APIView):
    pass

class CommunityList(APIView):
    def get(self, request):
        posts = UserPost.objects.all()
        serializer = UserPostSerializer(posts, many=True)
        print("serializer.data: ",serializer.data)
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

class ImageLikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, image_id):
        image = get_object_or_404(Image, image_id=image_id)
        like, created = ImageLike.objects.get_or_create(user=request.user, image=image)
        
        if created:
            # 只有在新创建点赞时才增加计数
            image.like_count = F('like_count') + 1
            image.save()
            return Response({
                'message': '图片点赞成功',
                'like_count': image.like_count + 1  # 因为F表达式，需要手动+1
            })
        return Response({
            'message': '您已经点赞过这张图片了',
            'like_count': image.like_count
        })

    def delete(self, request, image_id):
        image = get_object_or_404(Image, image_id=image_id)
        like = ImageLike.objects.filter(user=request.user, image=image)
        
        if like.exists():
            like.delete()
            image.like_count = F('like_count') - 1
            image.save()
            return Response({
                'message': '取消点赞成功',
                'like_count': image.like_count - 1  # 因为F表达式，需要手动-1
            })
        return Response({
            'message': '您还没有点赞这张图片',
            'like_count': image.like_count
        })


