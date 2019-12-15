from rest_framework import mixins
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination

from rest_framework.permissions import IsAdminUser

from .serializers import PostSerializer, UpdatePostSerializer
from blog.models import Post


class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    pagination_class=PageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'user__username', 'slug', ]


@api_view(['GET'])
def post_detail_api_view(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
         return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostUpdateView( mixins.UpdateModelMixin, generics.GenericAPIView):
    permission_classes = [IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = UpdatePostSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class PostDelete(mixins.DestroyModelMixin, generics.GenericAPIView):
    
    permission_classes = [IsAdminUser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
