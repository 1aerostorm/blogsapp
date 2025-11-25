from django.urls import path
from .views import AccountListCreateAPIView, PostListCreateAPIView, PostDetailAPIView

urlpatterns = [
    path('accounts/', AccountListCreateAPIView.as_view(), name='acc-list'),
    path('posts/', PostListCreateAPIView.as_view(), name='post-list'),
    path('posts/<int:post_id>/', PostDetailAPIView.as_view(), name='post-detail'),
]
