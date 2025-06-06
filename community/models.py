from django.db import models
from django.contrib.auth.models import User

class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images')
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('UserPost', on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f"Image {self.image_id} for post {self.post.title}"

class UserPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField()
    browse_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    like_users = models.ManyToManyField(User, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    like_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Comment {self.comment_id} on post {self.post.title}"
    

class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.TextField()
    post = models.ManyToManyField(UserPost)
    
    def __str__(self):
        return self.tag_name

class UserSavePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_posts')
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
        ordering = ['-saved_at']

    def __str__(self):
        return f"{self.user.username} saved {self.post.title}"
