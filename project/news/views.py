from django.shortcuts import render
from .models import *
#from django.views.generic import ListView, DetailView


def index(request):
    post = Post.objects.all()
    return render(request, 'index.html', context={'post': post})


def detail(request, title):
    info = Post.objects.get(title__iexact=title)
    return render(request, 'info.html', context={'info': info})


#class PostList(ListView):
    #model = Post
    #news_text = 'text'

    #template_name = 'index.html'
    #content_object_name = 'title'

#class PostDetail(DetailView):
    #model = Post
    #template_name = 'info.html'
    #context_object_name = 'title'