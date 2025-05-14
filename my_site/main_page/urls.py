from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name="home"),
    path('chat/', views.chat, name="chat"),
    path('post/<int:pk>', views.PostDetailView.as_view(), name="post"),
    path('post/create', views.create_post, name="post_create"),
    path('like/', views.post_or_comment_like),
]