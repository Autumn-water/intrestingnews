from django.http import Http404, JsonResponse
from django.shortcuts import render
from .models import Course
import os, hmac, hashlib, time
from django.conf import settings

def index(request):
    courses = Course.objects.filter(is_delete=False).all()
    return render(request, 'course/course.html', context={"courses": courses})


def detail(request, course_id):
    # /xxx/1    (query传参) /xxx/?course_id=
    # course_id = request.GET.get('news_id')
    try:
        # filter(id=course_id).first()  debug=False  会自动去找
        course = Course.objects.get(id=course_id)
        return render(request, 'course/course_detail.html', context={"course": course})
    except Course.DoesNotExist as e:
        raise Http404


def course_token(request):
    # http://192.168.31.200:8000/course/token/?video_url=
    # 获取视频路径
    video_url = request.GET.get('video_url')
    # video_url = 'http://ih2vvidjmihrie7nvje.exp.bcevod.com/mda-ih6x46pcj8w9vbs1/mda-ih6x46pcj8w9vbs1.m3u8'
    # 过期时间
    expiration_time = int(time.time()) + 3600
    # 百度云 UserId / UserKey
    user_id = settings.BAIDU_CLOUD_USER_ID
    user_key = settings.BAIDU_CLOUD_USER_KEY

    # extension ===> .mu38
    extension = os.path.splitext(video_url)[1]
    # mda-ih6x46pcj8w9vbs1.m3u8 ===>  mda-ih6x46pcj8w9vbs1
    media_id = video_url.split('/')[-1].replace(extension, '')

    # key 和 message 转化为 bytes str 转为 bytes
    key = user_key.encode('utf-8')
    message = '/{0}/{1}'.format(media_id, expiration_time).encode('utf-8')
    # 加密盐 加密数据  加密方式
    signature = hmac.new(key, message, digestmod=hashlib.sha256).hexdigest()
    token = '{0}_{1}_{2}'.format(signature, user_id, expiration_time)
    return JsonResponse({"token": token})

