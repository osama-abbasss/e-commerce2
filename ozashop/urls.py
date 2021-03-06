from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    #rest_framework
    path('api/blog/', include('blog.api.urls', namespace='api_blog')),




    path('', include('main.urls', namespace='main')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('search/', include('searches.urls', namespace='search')),

]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
