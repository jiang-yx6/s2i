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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/",views.UserLogin.as_view()),
    path("auth/register/",views.UserRegister.as_view()),
    path("auth/getuserinfo/",views.GetUserInfo.as_view()),
    
    path("getai/",views.AiDrawPicture.as_view()),

    path("posts/create/",community_views.CommunityPostCreate.as_view()),
    path("posts/list/",community_views.CommunityList.as_view()),
    path("posts/list/user/",community_views.CommunityListByUser.as_view()),
    path("posts/detail/<int:post_id>/",community_views.CommunityDetail.as_view()),
    path("posts/update/<int:post_id>/",community_views.CommunityUpdate.as_view()),
    path("posts/delete/<int:post_id>/",community_views.CommunityDelete.as_view()),
    path("posts/like/<int:post_id>/",community_views.CommunityLike.as_view()),
    path("posts/save/<int:post_id>/", community_views.SavePost.as_view()),

    path('comments/create/<int:post_id>/', community_views.CommentCreate.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
