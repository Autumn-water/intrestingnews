from django.urls import path
from . import views,course_view, doc_view, staff_view

app_name = 'admin'

urlpatterns = [
    path('', views.index, name="index"),
    # ajax 请求的url 建议都加上
    # path('edit-tag/', views.edit_news_tag, name="edit_news_tag"),  #  post
    path('news-tag-manage/', views.NewsTagView.as_view(), name="news_tag_manage"),
    path('news-pub/', views.NewsPubView.as_view(), name="news_pub"),
    path('news-edit/', views.NewsEditView.as_view(), name="news_edit"),
    path('up-token/', views.up_token, name="up_token"),
    path('upload-file/', views.upload_file, name="upload_file"),
    path('news-manage/', views.NewsManageView.as_view(), name="news_manage"),
    path('news-banner/', views.NewsBannerView.as_view(), name="news_banner"),
    path('news-hot/', views.NewsHotView.as_view(), name="news_hot"),
    path('news-hot-add/', views.NewsHotAddView.as_view(), name="news_hot_add"),
]


# 课堂相关的url
urlpatterns += [
    path('course-pub/', course_view.CoursePubView.as_view(), name="course_pub"),
    path('teacher-add/', course_view.add_teacher, name="add_teacher"),
]

# 文档
urlpatterns += [
    path('doc-upload/',doc_view.DocUploadView.as_view(), name="doc_upload"),
]

urlpatterns += [
    path('staff/', staff_view.Staff.as_view(), name="staff"),
    path('staff-add/', staff_view.StaffAdd.as_view(), name="staff_add"),
]