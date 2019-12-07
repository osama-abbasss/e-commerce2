from django.shortcuts import render
from .models import Searches
from blog.models import Post


def blog_search_qs(request):
    query = request.GET.get('q', None) #q is the name in search form html
    
    user = None
    if request.user.is_authenticated:
        user = request.user
    context = {'query': query}
    if query is not None:
       searches = Searches.objects.create(user= user ,query=query)
       blog_list = Post.objects.search(query=query)
       context['blog_list'] = blog_list
    
    return render(request, 'searches/blog_search.html', context)
