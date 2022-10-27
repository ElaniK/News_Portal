from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from .models import *

from django.views.generic import ListView, DetailView
from .models import *

class AuthorList(ListView):
    model = Author
    context_object_name = 'Authors'
    #queryset = Author.objects.all()
    template_name = 'news/author_list.html'

class Post(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'




