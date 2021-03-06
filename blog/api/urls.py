from django.urls import path
from .views import PostList, post_detail_api_view, PostUpdateView, PostDelete

app_name = 'api_blog'

urlpatterns = [
    path('', PostList.as_view(), name='api_detail'),
    path('<slug>/', post_detail_api_view, name='api_detail'),
    path('update/<pk>/', PostUpdateView.as_view(), name='update'),
    path('delete/<pk>/', PostDelete.as_view(), name='delete'),
]
