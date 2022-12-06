from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .filters import *
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.core.cache import cache




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
    paginate_by = 2  # указываем количество записей на странице


class ShowPost(DetailView):
    model = Post
    template_name = 'news/info.html'
    # pk_url_kwarg: str = "pk"
    context_object_name = 'info'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'Post-{self.kwargs["pk"]}',
                        None)  # метод get забирает значение по ключу, если его нет, то забирает None.

        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'Post-{self.kwargs["pk"]}', obj)

        return obj


class SearchPost(ListView):
    model = Post
    template_name = 'news/search.html'
    context_object_name = 'search'
    paginate_by = 2  # указываем количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# def create_post(request):
#     if request.method =='POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#
#     form = PostForm
#     return render(request, 'create.html', {'form': form})


class CreatePost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    model = Post
    template_name = 'news/create.html'
    form_class = PostForm


class UpdatePost(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    model = Post
    template_name = 'news/create.html'
    form_class = PostForm


class DeletePost(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'news/delete.html'
    success_url = reverse_lazy('post_list')
    context_object_name = 'del_post'


class CategoryList(ListView):
    model = Post
    template_name = 'news/categories.html'
    context_object_name = 'categories'
    paginate_by = 5

    def get_queryset(self):  # фильтрация по категории
        # выдаст ошибку 404, если категории не существует
        self.postCategory = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.postCategory).order_by('dateCreation')
        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscribe'] = self.request.user not in self.postCategory.subscribers.all()
        context['postCategory'] = self.postCategory
        return context

#подписка на группу
@login_required
def add_subscribe(request, **kwargs):
    category_number = int(kwargs['pk'])
    Category.objects.get(pk=category_number).subscribers.add(request.user)

    return redirect('/news/')

#отписка на группу
@login_required
def delete_subscribe(request, **kwargs):
    category_number = int(kwargs['pk'])
    Category.objects.get(pk=category_number).subscribers.remove(request.user)

    return redirect('/news/')