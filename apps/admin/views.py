from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils import json_status
from apps.news.models import NewsTag, News, NewsHot, NewsBanner
from django.http import QueryDict
from qiniu import Auth
from django.http import JsonResponse
from django.conf import settings
import os
from .forms import NewsPubForm, NewsHotAddForm, NewsEditForm, NewsBannerForm
from utils.decorators import ajax_login_required, user_permission_required
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from urllib.parse import urlencode


# 必须是员工  is_staff
@staff_member_required(login_url='/account/login/')
def index(request):
    return render(request, 'admin/index.html')


# 类视图
@method_decorator([csrf_exempt, staff_member_required(login_url='/account/login/'), user_permission_required(NewsTag)],
                  name="dispatch")
class NewsTagView(View):

    def get(self, request):
        # is_delete 删了 True
        news_tags = NewsTag.objects.filter(is_delete=False).all()
        return render(request, 'admin/news/news_tag_manage.html', context={"news_tags": news_tags})

    def post(self, request):
        # 取值 name 已经在表存在了 再次输入 提示已经存在
        name = request.POST.get("name")
        # print(name) python 怎么去字符串空格 给空格会被过滤掉 后台的最后一道验证
        if name and bool(name.strip()):
            # exists 是否存  True / False  平时都是一些逻辑
            news_tag_exists = NewsTag.objects.filter(name=name).exists()
            if news_tag_exists:
                return json_status.params_error(message="该标签已经存在,请不要重复输入")
            # 创建数据 成功的标准(怎么样确保成功)
            NewsTag.objects.create(name=name)
            return json_status.result(message="成功")
        return json_status.params_error(message="标签名不能为空")

    def put(self, request):
        """
        # 接收前端 put 请求的值  post
        # request.PUI 没有
        # request.POST
        # <QueryDict: {'tag_name': ['技']}>
        # 所有的参数 全部是存在body POST/GET b'tag_name=%E6%8A%80'
        # 我是采用id来判断
        # 在前端向后台提供了只有两个tag_id(标签id) tag_name  (标签name)
        :param request:
        :return:
        """
        res = QueryDict(request.body)
        tag_name = res.get("tag_name", None)
        tag_id = res.get("tag_id", None)
        if tag_id and tag_name:
            tag = NewsTag.objects.filter(id=tag_id)
            if tag:
                news_tag_exists = NewsTag.objects.filter(name=tag_name).exists()
                if news_tag_exists:
                    return json_status.params_error(message="该标签已经存在,请不要重复输入")
                tag.update(name=tag_name)
                return json_status.result()
            return json_status.params_error(message="标签不存在")
        return json_status.params_error(message="标签不存在")

    def delete(self, request):
        res = QueryDict(request.body)
        # 前端只传了 tag_id  (tagId 错误的)
        tag_id = res.get("tag_id", None)
        tag = NewsTag.objects.filter(id=tag_id)
        # 防止有的人 绕过浏览器
        if tag_id and tag:
            tag.update(is_delete=True)
            return json_status.result()
        return json_status.params_error(message="标签不存在")


# 开一个新路由 用来操作  put（更改） / post （添加） 需要对应一个 url
def edit_news_tag(request):
    # post request.POST.get("tag_id)
    # post request.POST.get("tag_name)
    tag_name = request.POST.get("tag_name", None)
    tag_id = request.POST.get("tag_id", None)
    if tag_id and tag_name:
        tag = NewsTag.objects.filter(id=tag_id)
        if tag:
            news_tag_exists = NewsTag.objects.filter(name=tag_name).exists()
            if news_tag_exists:
                return json_status.params_error(message="该标签已经存在,请不要重复输入")
            tag.update(name=tag_name)
            return json_status.result()
        return json_status.params_error(message="标签不存在")
    return json_status.params_error(message="标签不存在")


#
# def del_news_tag(request):
#     pass


@method_decorator([csrf_exempt, staff_member_required(login_url='/account/login/'), user_permission_required(News)],
                  name="dispatch")
class NewsPubView(View):

    def get(self, request):
        news_tags = NewsTag.objects.filter(is_delete=False).all()
        return render(request, 'admin/news/news_pub.html', context={"news_tags": news_tags})

    def post(self, request):
        # 验证数据 form request.POST传进去
        form = NewsPubForm(request.POST)
        # cleaned_data 写在验证前面 是获取不到值
        if form.is_valid():
            # title  经过Form验证 如果说没通用验证
            # title1 = request.POST.get("title")
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            tag_id = form.cleaned_data.get('tag_id')
            thumbnail_url = form.cleaned_data.get('thumbnail_url')
            content = form.cleaned_data.get('content')
            # 去查出来 tag
            tag = NewsTag.objects.filter(id=tag_id).first()
            # print(title)
            # print(desc)
            # print(tag)
            # print(thumbnail_url)
            # print(content)
            # 当前用户 request.user  user.xxx
            if tag:
                News.objects.create(title=title, desc=desc, tag=tag, thumbnail_url=thumbnail_url, content=content,
                                    author=request.user)
                return json_status.result()
            return json_status.params_error(message="标签不存在")
        # form 没有这个 get_error
        print(form.errors)
        return json_status.params_error(message=form.get_error())


@method_decorator([csrf_exempt, staff_member_required(login_url='/account/login/'), user_permission_required(News)],
                  name="dispatch")
class NewsEditView(View):
    """新闻的编辑"""

    def get(self, request):
        news_id = request.GET.get('news_id')
        if news_id:
            news = News.objects.filter(id=news_id).first()
            if news:
                news_tags = NewsTag.objects.filter(is_delete=False).all()
                context = {"news": news, "news_tags": news_tags}
                return render(request, 'admin/news/news_pub.html', context=context)
            return json_status.params_error(message="新闻找不到")
        return json_status.params_error(message="新闻id错误")

    def post(self, request):
        # Form
        form = NewsEditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            desc = form.cleaned_data.get('desc')
            tag_id = form.cleaned_data.get('tag_id')
            thumbnail_url = form.cleaned_data.get('thumbnail_url')
            content = form.cleaned_data.get('content')
            news_id = form.cleaned_data.get('news_id')
            news = News.objects.filter(id=news_id)
            if news:
                tag = NewsTag.objects.filter(id=tag_id).first()
                news.update(title=title, desc=desc, tag=tag, thumbnail_url=thumbnail_url, content=content,
                            author=request.user)
                return json_status.result()
            return json_status.params_error(message="新闻不存在")
        return json_status.params_error(message=form.get_error())


# 1. 安装 pip install qiniu
def up_token(request):
    # 如何返回 token
    # 需要填写你的 Access Key 和 Secret Key
    access_key = settings.QI_NIU_ACCESS_KEY
    secret_key = settings.QI_NIU_SECRET_KEY
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = settings.QI_NIU_BUCKET_NAME
    # 3600为token过期时间，秒为单位。3600等于一小时
    token = q.upload_token(bucket_name)
    return JsonResponse({"uptoken": token})


# 仅仅写了 view  / url
# @method_decorator([], name="dispatch") # 会报错
# @staff_member_required() # 是针对  form /get/post/ 不能处理ajax  ajax 自己写
# 自己用自定义装饰器 专门处理ajax请求
@ajax_login_required  # 只要没登录 {code: 403, msg: "请先登录", data: null} 前端根据 code 值进行判断
def upload_file(request):
    # request.FILES (任何文件都会存在这里面 ) request.POST body(请求体)
    file = request.FILES.get('upload_file')
    # <class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
    # <class 'django.core.files.uploadedfile.TemporaryUploadedFile'>
    # django 对于你上传图片大小 会选择对应的 对象来  图形小于 2.5m
    # print('==========')
    # print(file)  # 2018.png
    # print(file.name)  # 2018.png
    # print(type(file))
    # print(type(file.name))
    # print('==========')
    # 文件名
    file_name = file.name
    # file_path 文件保存
    # x/media/加密字符串.png
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    with open(file_path, 'wb') as f:
        # file.chunks() 返回的是一个生成器 能被生成器 不会一次全部使用
        for chunk in file.chunks():
            f.write(chunk)
    # 返回地址  http://192.168.31.200:8000 /media/xxx + settings.MEDIA_URL+file_name
    file_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)
    # http://192.168.31.200:8000/admin/upload-file/ 当前视图对应的绝对路径
    print(request.build_absolute_uri())
    # return JsonResponse({"file_url": file_url})
    return json_status.result(data={"file_url": file_url})


# https://docs.djangoproject.com/en/2.1/howto/static-files/

@method_decorator([csrf_exempt, staff_member_required(login_url='/account/login/'), user_permission_required(News)],
                  name="dispatch")
class NewsManageView(View):

    def get(self, request):
        p = int(request.GET.get('p', 1))
        newses = News.objects.defer('content').select_related('tag', 'author')
        # 获取前端传过来的参数
        start_time = request.GET.get('start_time', '')
        end_time = request.GET.get('end_time', '')
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        tag_id = int(request.GET.get('tag_id', 0))
        # 开始时间 结束时间有值
        if start_time and end_time:
            # 把 2018/09/26 转成 datetime
            start_date = datetime.strptime(start_time, '%Y/%m/%d')
            # 加一天
            end_date = datetime.strptime(end_time, '%Y/%m/%d') + timedelta(days=1)
            # 2018-10-25 00:00:00 2018-10-25 00:00:00 + 1 == 2018-10-26 00:00:00
            # print(start_date, end_date)
            # print(type(start_date))
            # 去数据库过滤 过滤出新闻在 开始时间和结束时间 之间
            from django.utils.timezone import make_aware
            newses = newses.filter(pub_time__range=(make_aware(start_date), make_aware(end_date)))

        if title:
            # title = “新闻标签123A”
            print(1)
            newses = newses.filter(title__icontains=title)

        if author:
            print(2)
            # 用户名匹配
            newses = newses.filter(author__username__icontains=author)

        # 这一步
        if tag_id:
            newses = newses.filter(tag=tag_id)

        news_tags = NewsTag.objects.filter(is_delete=False).all()
        paginator = Paginator(newses, settings.ONE_PAGE_NEWS_COUNT)
        # print('===============')
        print('总数量', paginator.count)
        # print('可以被迭代的页码', paginator.page_range)
        # # for i in paginator.page_range:
        #     # print(i) # 1-2
        # print('总页数', paginator.num_pages)
        # print('===============')
        page = paginator.page(p)
        # print('**********************')
        # print('当前处在的页码', page.number)
        print('当页数据', page.object_list)
        # print('是否具有下一页', page.has_next())
        # print('是否具有上一页', page.has_previous())
        # if page.has_next():
        #     print('下一页的页码', page.next_page_number())
        # if page.has_previous():
        #     print('上一页的页码', page.previous_page_number())
        # print('是否具有其他页面', page.has_other_pages())
        # print('开始位置的索引', page.start_index())
        # print('结束位置的索引', page.end_index())
        #
        # print('**********************')
        page_data = self.get_page_data(paginator, page)
        context = {
            "newses": page.object_list,
            "news_tags": news_tags,
            "paginator": paginator,
            "page": page,
            "start_time": start_time,
            "end_time": end_time,
            "title": title,
            "author": author,
            "tag_id": tag_id,
            # start_time=start_time&end_time=end_time
            "other_param": urlencode({
                "start_time": start_time,
                "end_time": end_time,
                "title": title,
                "author": author,
                "tag_id": tag_id,
            })
        }
        context.update(page_data)
        # print('-====--------------------')
        # print(page_data)
        # print('-====--------------------')
        return render(request, 'admin/news/news_manage.html', context=context)

    @staticmethod
    def get_page_data(paginator, page, around_count=2):

        # 获取当页所在的页码
        current_page = page.number
        # 获取总的页数
        total_page = paginator.num_pages

        # 标志位 flag
        left_has_more = False
        right_has_more = False

        # 算出当前页面左边的页码 6
        left_start_index = current_page - around_count
        left_end_index = current_page
        if current_page <= around_count + around_count + 1:
            # range(6-2, 6)
            left_pages = range(1, left_end_index)
        else:
            left_has_more = True
            left_pages = range(left_start_index, left_end_index)

        # 右边 range(1, 2) 分页一种 是前端实现  后端实现
        right_start_index = current_page + 1
        right_end_index = current_page + around_count + 1
        if current_page >= total_page - around_count - around_count:
            right_pages = range(right_start_index, total_page + 1)
        else:
            right_has_more = True
            right_pages = range(right_start_index, right_end_index)

        return {
            "current_page": current_page,
            "total_page": total_page,
            "left_has_more": left_has_more,
            "right_has_more": right_has_more,
            "left_pages": left_pages,
            "right_pages": right_pages
        }

    def delete(self, request):
        from django.http import QueryDict
        res = QueryDict(request.body)
        news_id = res.get('news_id')
        if news_id:
            news = News.objects.filter(id=news_id).first()
            if news:
                # 为什么要加这一步 NewsHot 热门新闻 如果说你把新闻删了 热门新闻
                # 业务逻辑
                hot_news = NewsHot.objects.filter(news=news)
                if hot_news:
                    hot_news.update(is_delete=True)
                news.is_delete = True
                news.save()
                return json_status.result()
            return json_status.params_error(message="新闻不存在")
        return json_status.params_error(message="参数错误")


# get/post  遵循restful  get/post/put/delete
@method_decorator([csrf_exempt, user_permission_required(NewsHot)], name="dispatch")
class NewsHotView(View):
    def get(self, request):
        return render(request, 'admin/news/news_hot.html')

    def put(self, request):
        ret = QueryDict(request.body)
        priority = int(ret.get('priority', 0))
        if priority:
            hot_news_id = int(ret.get('hot_news_id', 0))
            hot_news = NewsHot.objects.filter(id=hot_news_id)
            if hot_news:
                hot_news.update(priority=priority)
                return json_status.result()
            return json_status.params_error(message='热门新闻不存在')
        return json_status.params_error(message="优先级错误")

    def delete(self, request):
        ret = QueryDict(request.body)
        hot_news_id = int(ret.get('hot_news_id', 0))
        hot_news = NewsHot.objects.filter(id=hot_news_id)
        if hot_news:
            # hot_news.delete()
            hot_news.update(is_delete=True)
            return json_status.result()
        return json_status.params_error(message='热门新闻不存在')


@method_decorator([csrf_exempt, user_permission_required(NewsHot)], name="dispatch")
class NewsHotAddView(View):
    def get(self, request):
        return render(request, 'admin/news/news_hot_add.html')

    def post(self, request):
        form = NewsHotAddForm(request.POST)
        if form.is_valid():
            news_id = form.cleaned_data.get('news_id')
            priority = form.cleaned_data.get('priority')
            news = News.objects.filter(id=news_id).first()
            if news:
                hot_news = NewsHot.objects.filter(news=news).exists()
                if hot_news:
                    return json_status.params_error(message="该新闻已经是热门新闻")
                NewsHot.objects.create(priority=priority, news=news)
                return json_status.result()
            return json_status.params_error(message="新闻不存在")
        print(form.errors)
        return json_status.params_error(message=form.get_error())


@method_decorator([csrf_exempt, user_permission_required(NewsBanner)], name="dispatch")
class NewsBannerView(View):
    def get(self, request):
        return render(request, 'admin/news/news_banner.html')

    def post(self, request):
        form = NewsBannerForm(request.POST)
        if form.is_valid():
            link_to = form.cleaned_data.get("link_to")
            image_url = form.cleaned_data.get('image_url')
            priority = form.cleaned_data.get('priority')
            print('link_to:{},image_url:{},priority:{} '.format(link_to, image_url, priority))
            banner = NewsBanner.objects.create(image_url=image_url, priority=priority, link_to=link_to)
            return json_status.result(data={"banner_id": banner.id, "priority": priority})
        return json_status.params_error(message=form.get_error())

    def put(self, request):
        p = QueryDict(request.body)
        banner_id = p.get("banner_id")
        image_url = p.get("image_url")
        priority = p.get("priority")
        link_to = p.get("link_to")
        if banner_id:
            # first / all
            banner = NewsBanner.objects.filter(id=banner_id)
            if banner:
                banner.update(image_url=image_url, priority=priority, link_to=link_to)
                return json_status.result()
            return json_status.result().params_error(message='轮播图找不到')
        return json_status.result().params_error(message="bannerId不存在")

    def delete(self, request):
        d = QueryDict(request.body)
        banner_id = d.get("banner_id")
        if banner_id:
            banner = NewsBanner.objects.filter(id=banner_id)
            if banner:
                banner.update(is_delete=True)
                return json_status.result()
            return json_status.params_error(message="轮播图不存在")
        return json_status.params_error(message="轮播图id不存在")
