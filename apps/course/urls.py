from django.urls import path, re_path
from .views import index, detail, course_token

app_name = 'course'

urlpatterns = [
    path('', index, name="index"),
    path('detail/<int:course_id>/', detail, name="detail"),
    path('token/', course_token, name="course_token"),
]
