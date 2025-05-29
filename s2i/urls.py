"""
URL configuration for s2i project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from myapp import views
from community import views as community_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/",views.UserLogin.as_view()),
    path("auth/register/",views.UserRegister.as_view()),
    # path("upload/voice",views.VoiceFileUpload.as_view()),
    # path("upload/avatar",views.AvatarUpload.as_view()),
    
    path("getai/",views.AiDrawPicture.as_view()),

    path("posts/create/",community_views.CommunityPostCreate.as_view()),
    path("posts/list/",community_views.CommunityList.as_view()),
    path("posts/detail/<int:pk>/",community_views.CommunityDetail.as_view()),
    path("posts/update/<int:pk>/",community_views.CommunityUpdate.as_view()),
    path("posts/delete/<int:pk>/",community_views.CommunityDelete.as_view()),
    path("posts/like/<int:pk>/",community_views.CommunityLike.as_view()),
    path("posts/save/<int:pk>/", community_views.SavePost.as_view()),
    path('images/<int:image_id>/like/', community_views.ImageLikeView.as_view(), name='image-like'),

]
