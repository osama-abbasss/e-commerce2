from django.urls import path
from .views import blog_search_qs
app_name = 'search'

urlpatterns = [
    path('', blog_search_qs, name='search')
]

