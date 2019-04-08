from django.db import models


class Teacher(models.Model):
    # 讲师名
    name = models.CharField(max_length=10)
    # 讲师身份
    identity = models.CharField(max_length=100)
    # 简介
    profile = models.TextField()
    # 头像地址
    avatar_url = models.URLField()
    # 加入时间
    join_date = models.DateTimeField(auto_now_add=True)
    # 是否删除
    is_delete = models.BooleanField(default=False)


class CourseCategory(models.Model):
    # 分类名
    name = models.CharField(max_length=20)
    # 是否删除
    is_delete = models.BooleanField(default=False)


class Course(models.Model):
    # 课程标题
    title = models.CharField(max_length=100)
    # 课程封面图
    cover_url = models.URLField()
    # 课程视频地址
    video_url = models.URLField()
    # 课程时长
    duration = models.FloatField()
    # 课程简介
    profile = models.TextField(null=True, blank=True)
    # 课程大纲
    outline = models.TextField(null=True, blank=True)
    # 创建时间
    create_time = models.DateTimeField(auto_now_add=True)
    # 是否删除
    is_delete = models.BooleanField(default=False)

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
