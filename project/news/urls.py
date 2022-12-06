from django.urls import path
#from .views import index, detail
from .views import (
    PostList, ShowPost, SearchPost, UpdatePost, DeletePost, CreatePost, CategoryList,
    add_subscribe, delete_subscribe,
)
from django.views.decorators.cache import cache_page

urlpatterns = [
    # path('news_list/', index, name='index'),
    # path('info/<str:title>/', detail, name='detail'),

    path('', cache_page(60)(PostList.as_view()), name='post_list'),
    path('info/<int:pk>/', ShowPost.as_view(), name='show_post'),
    path('search/', SearchPost.as_view(), name='search_post'),
    path('create/', CreatePost.as_view(), name='create_post'),
    path('update/<int:pk>/', UpdatePost.as_view(), name='update_post'),
    path('delete/<int:pk>/', DeletePost.as_view(), name='delete_post'),
    path('categories/<int:pk>/', cache_page(300)(CategoryList.as_view()), name='category_list'),
    path('categories/<int:pk>/add_sub/', add_subscribe, name='add_subscribe'),
    path('categories/<int:pk>/del_sub/', delete_subscribe, name='delete_subscribe'),
]

