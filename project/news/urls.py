from django.urls import path
from .views import index, detail
#from .views import PostList, PostDetail

urlpatterns = [
    path('news_list/', index, name='index'),
    path('info/<str:title>/', detail, name='detail'),

    #path('news_list/', PostList.as_view()),
    #path('info/', PostDetail.as_view())

]