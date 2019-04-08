from django.http import HttpResponse
from apps.course.models import Teacher, Course, CourseCategory
from django.views import View
from django.shortcuts import render
from .forms import CoursePubForm
from utils import json_status
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils.decorators import user_permission_required


def add_teacher(request):
    name = 'Which'
    identity = '讲师'
    profile = '人生苦短，我用Python'
    avatar_url = 'http://onj3s3zfw.bkt.clouddn.com/o_1cmnijm1ksft19ir1et96oaib7.png'
    Teacher.objects.create(name=name, identity=identity, profile=profile, avatar_url=avatar_url)
    return HttpResponse("ok")


@method_decorator([csrf_exempt, user_permission_required(Course) ], name="dispatch")
class CoursePubView(View):

    def get(self, request):
        teachers = Teacher.objects.filter(is_delete=False).all()
        categories = CourseCategory.objects.filter(is_delete=False).all()
        context = {
            "teachers": teachers,
            "categories": categories,
        }
        return render(request, 'admin/course/course_pub.html', context=context)

    def post(self, request):
        form = CoursePubForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            video_url = form.cleaned_data.get("video_url")
            cover_url = form.cleaned_data.get("cover_url")
            teacher_id = form.cleaned_data.get("teacher_id")
            # name=teacher_name
            teacher = Teacher.objects.filter(id=teacher_id).first()
            duration = form.cleaned_data.get('duration')
            profile = form.cleaned_data.get("profile")
            outline = form.cleaned_data.get("outline")
            category_id = form.cleaned_data.get('category_id')
            # category 分类
            category = CourseCategory.objects.filter(id=category_id).first()
            course = Course.objects.create(title=title, video_url=video_url, cover_url=cover_url, teacher=teacher, duration=duration, profile=profile, outline=outline, category=category)
            return json_status.result(data={"course_id": course.id})
        print(form.errors)
        return json_status.params_error(message=form.get_error())