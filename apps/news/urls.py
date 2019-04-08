from django.urls import path
# from .views import index, search
from . import views
# app的名字
app_name = 'news'
# reverse('news:index')

urlpatterns = [
    path('', views.index, name="index"),
    path('news/detail/<int:news_id>', views.news_detail, name="news_detail"),
    path('news/add-comment/', views.AddNewsCommentView.as_view(), name="add_news_comment"),
    path('news/comment/', views.comment_list_with_news, name="comment_list_with_news"),
    path('news/list/', views.news_list, name="news_list"),
    path('news/tag/list/', views.news_tag_list, name="news_tag_list"),
    path('news/news-with-tag/', views.news_with_tag, name="news_with_tag"),
    path('news/hot/list/', views.hot_news_list, name="hot_news_list"),
    path('news/banner/list/', views.news_banner_list, name="news_banner_list"),
    path('search/', views.search, name="search"),
]
