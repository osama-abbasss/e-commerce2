from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment
from .forms import  PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, DetailView,
                                  DeleteView, UpdateView,
                                  View, CreateView)


class PostListView(ListView):
    model = Post
    paginate_by= 5
    template_name = 'blog/blog.html'


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/single-blog.html'
    comment_form = CommentForm()


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_blog.html'
    form_class = PostForm

    success_url = "/blog/"


class PostEditeView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create_blog.html'
    form_class = PostForm
    success_url = "/"


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_blog.html'
    success_url = reverse_lazy("/")



@login_required
def add_comment_to_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            message = form.cleaned_data.get('comment')
            comment = Comment(user = request.user,
                                comment= message,
                                post=post)
            comment.save()
            return redirect('blog:single_post', slug=slug)
    else:
        form = CommentForm()

    context = {'comment_form':form}
    return render (request, 'blog/comment_form.html', context)



class DetailView(View):
    def get(self, *args, **kwargs):
        post_qs = Post.objects.all()
        post = Post.objects.filter(slug=post_qs.slug)

        return render(self.request, 'blog/single-blog.html', context)

    def post(self, *args, **kwargs):
        pass

