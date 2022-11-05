from django.urls import path
#from .views import index, detail
from .views import PostList, ShowPost, SearchPost, create_post

urlpatterns = [
    # path('news_list/', index, name='index'),
    # path('info/<str:title>/', detail, name='detail'),

    path('', PostList.as_view()),
    path('info/<int:pk>/', ShowPost.as_view()),
    path('search/', SearchPost.as_view()),
    path('create/', create_post),


]

