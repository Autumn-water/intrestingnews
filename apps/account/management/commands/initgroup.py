from django.core.management.base import BaseCommand
from apps.news.models import NewsHot, News, NewsBanner, NewsTag, NewsComment
from apps.course.models import Course, Teacher, CourseCategory
from apps.doc.models import Doc
# 下面这个 导入django内置的模型 Group ContentType 关联模型和app 自定义account.User 普通的
from django.contrib.auth.models import Group, Permission, ContentType


#  运营组/课程组/管理员组
#  运营组: 负责发表新闻，日常维护
#  课程组: 负责发布课程，上传文档
#  管理员: 运营组+课程组
class Command(BaseCommand):
    def handle(self, *args, **options):
        # 运营组
        # 会产生一个对象  创建用户的时候 update/delete(返回True/False)
        # News.object.create()
        yy_group = Group.objects.create(name='运营组')
        # 根据模型找权限 多对多
        yy_content_types = [
            ContentType.objects.get_for_model(NewsComment),
            ContentType.objects.get_for_model(NewsHot),
            ContentType.objects.get_for_model(News),
            ContentType.objects.get_for_model(NewsBanner),
            ContentType.objects.get_for_model(NewsTag),
        ]
        # 查找权限
        yy_permissions = Permission.objects.filter(content_type__in=yy_content_types)
        # 通过 set 来设置权限
        yy_group.permissions.set(yy_permissions)

        # 课程组 有多个权限 是一个列表
        ck_group = Group.objects.create(name='课程组')
        ck_content_types = [
            ContentType.objects.get_for_model(Doc),
            ContentType.objects.get_for_model(CourseCategory),
            ContentType.objects.get_for_model(Course),
            ContentType.objects.get_for_model(Teacher),
        ]
        ck_permissions = Permission.objects.filter(content_type__in=ck_content_types)
        ck_group.permissions.set(ck_permissions)

        # 创建管理员组  课程 和 运营
        admin_group = Group.objects.create(name='管理员')
        # 进行拼接
        admin_permissions = yy_permissions.union(ck_permissions)
        admin_group.permissions.set(admin_permissions)
        self.stdout.write(self.style.SUCCESS("分组初始化成功"))
