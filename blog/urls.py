from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name= 'all_posts'),
    path('<slug>/', views.PostDetailView.as_view(), name='single_post'),
    path('create/', views.PostCreateView.as_view(), name='create_post'),
    path('edite/<slug>/', views.PostEditeView.as_view(), name='edite_post'),
    path('delete/<slug>/', views.PostDeleteView.as_view(), name='delete_post'),
    path('comment/<slug>/', views.add_comment_to_post, name='comment_to_post'),
]
