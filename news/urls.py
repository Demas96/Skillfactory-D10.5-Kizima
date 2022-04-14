from django.urls import path
from .views import PostList, Search, PostCreateView, PostDetailView, PostUpdateView, PostDeleteView, SubscribeView

urlpatterns = [
    path('', PostList.as_view()),
    path('search/', Search.as_view()),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('add/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
]