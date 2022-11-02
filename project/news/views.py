#from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView


# def index(request):
#     post = Post.objects.all()
#     return render(request, 'index.html', context={'post': post})
#
#
# def detail(request, title):
#     info = Post.objects.get(title__iexact=title)
#     return render(request, 'info.html', context={'info': info})


class PostList(ListView):
    model = Post
    template_name = 'news/index.html'
    context_object_name = 'post'

class ShowPost(DetailView):
    model = Post
    template_name = 'news/info.html'
    #pk_url_kwarg: str = "pk"
    context_object_name = 'info'