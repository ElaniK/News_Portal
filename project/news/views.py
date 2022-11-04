#from django.shortcuts import render
from .models import *
from django.views.generic import ListView, DetailView
from .filters import *

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
    paginate_by = 2 # указываем количество записей на странице


class ShowPost(DetailView):
    model = Post
    template_name = 'news/info.html'
    #pk_url_kwarg: str = "pk"
    context_object_name = 'info'

class SearchPost(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'serach'
    paginate_by = 2 # указываем количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context