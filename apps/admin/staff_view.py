from django.views import View
from django.shortcuts import render
from utils import json_status
from utils.decorators import user_permission_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.account.models import User
from django.db.models import Q
from utils.decorators import is_super_user_required
from django.contrib.auth.models import Group
from django.views.decorators.csrf import csrf_exempt


# 员工相关 只能是炒鸡管理员
@method_decorator([login_required, is_super_user_required], name='dispatch')
class Staff(View):
    def get(self, request):
        # 查出所有的员工和炒鸡管理员
        staffs = User.objects.filter(Q(is_superuser=True) | Q(is_staff=True)).all()
        return render(request, 'admin/staff.html', context={"staffs": staffs})


@method_decorator([is_super_user_required, csrf_exempt], name="dispatch")
class StaffAdd(View):

    def get(self, request):
        groups = Group.objects.all()
        print(groups)
        return render(request, 'admin/staff_add.html', context={"groups": groups})

    def post(self, request):
        # 获取手机号
        telephone = request.POST.get("telephone")
        # 得到用户 查出用户
        user = User.objects.filter(telephone=telephone).first()
        if user:
            # 获取（权限）列表组 [1,2 ]
            groups_ids = request.POST.getlist('groups')
            if groups_ids:
                # 过滤选中的组 id__in 这个在不在 [1, 2]
                group = Group.objects.filter(id__in=groups_ids)
                # 设置组
                user.groups.set(group)
                # 设置为员工
                user.is_staff = True
                user.save()
                return json_status.result()
            return json_status.params_error('至少选一个分组')
        return json_status.params_error('该用户不存在，请先注册后再添加')
