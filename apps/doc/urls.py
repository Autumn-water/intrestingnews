from django.urls import path
from .views import index, download_doc

app_name = 'doc'


urlpatterns = [
    path('', index, name="index"),
    path('download/', download_doc, name="download_doc"),
]
