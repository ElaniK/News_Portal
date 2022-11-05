from django.urls import path
#from .views import index, detail
from .views import (
    PostList, ShowPost, SearchPost,UpdatePost, DeletePost
)

urlpatterns = [
    # path('news_list/', index, name='index'),
    # path('info/<str:title>/', detail, name='detail'),

    path('', PostList.as_view(), name='post_list'),
    path('info/<int:pk>/', ShowPost.as_view(), name='show_post'),
    path('search/', SearchPost.as_view(), name='search_post'),
    path('create/', CreatePost.as_view(), name='create_pst'),
    path('update/<int:pk>/', UpdatePost.as_view(), name='update_post'),
    path('delete/<int:pk>/', DeletePost.as_view(), name='delete_post'),


]

