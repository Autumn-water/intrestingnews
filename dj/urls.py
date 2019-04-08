"""djT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include('apps.news.urls')),
    path('course/', include('apps.course.urls')),
    path('doc/', include('apps.doc.urls')),
    path('account/', include('apps.account.urls')),
    path('admin/', include('apps.admin.urls')),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)[0],
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# [1, 2] + [3, 4] = [1, 2, 3,4 ] 是为了 static 如果说你没有配置static STATIC_DIRS
# [1, 2, [3, 4]]
