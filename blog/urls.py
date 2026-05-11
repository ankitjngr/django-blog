from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_api, name='register'),
    path('posts/', views.post_list, name='post-list'),
    path('posts/<int:post_id>/', views.post_detail, name='post-detail'),
    path('posts/<int:pk>/comment/', views.comment_list, name='comment-list'),
    path('posts/<int:pk>/like/', views.like_post, name='like-post'),
    path('profile/', views.userprofile, name='user-profile'),
]
