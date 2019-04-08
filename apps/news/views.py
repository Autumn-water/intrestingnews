from django.shortcuts import render
from django.views import View
from .models import NewsTag, News, NewsComment, NewsHot, NewsBanner
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods
from .forms import AddNewsCommentFrom
from utils import json_status
from .serializers import NewsCommentSerializer, NewsSerializer, NewsTagSerializer, NewsHotSerializer, \
    NewsBannerSerializer
from django.contrib.auth.decorators import login_required
from utils.decorators import ajax_login_required
from django.conf import settings
from django.db.models import Q

@require_GET
def index(request):
    # 新闻标签 新闻
    # select id, pub_time   is_delete True=> False 语义错误 先设计好模型  就不动
    news_tags = NewsTag.objects.filter(is_delete=False).all()
    newses = News.objects.defer('content').select_related('tag', 'author').filter(is_delete=False).all()[0:settings.ONE_PAGE_NEWS_COUNT]
    # 查出 banner 查出热门新闻
    # all()
    h_newses = NewsHot.objects.filter(is_delete=False).all()
    banners = NewsBanner.objects.filter(is_delete=False).all()
    context = {
        "news_tags": news_tags,
        "newses": newses,
        "h_newses": h_newses,
        "banners": banners,
    }
    # from datetime import datetime
    # from django.utils.timezone import now
    # print(now())   # django 提供 2018-10-19 13:24:49.499108+00:00  + 8
    # print(datetime.now())  # 2018-10-19 21:24:49.499366 系统 不准确
    return render(request, 'news/index.html', context=context)


# 用来做分页 加载更多
def news_list(request):
    page = int(request.GET.get('page', 1))
    tag_id = int(request.GET.get('tag_id', 0))
    # 计算一页 一开始默认就已经加载一页 开始位置 结束位置  1 * 1
    start_index = settings.ONE_PAGE_NEWS_COUNT * (page - 1)
    end_index = start_index + settings.ONE_PAGE_NEWS_COUNT
    # print(start_page, end_page)
    if tag_id:
        newses = News.objects.defer('content').select_related('tag', 'author').filter(is_delete=False, tag=tag_id).all()[start_index:end_index]
    else:
        newses = News.objects.defer('content').select_related('tag', 'author').filter(is_delete=False).all()[start_index:end_index]
    # 返回序列化数据
    serializer = NewsSerializer(newses, many=True)
    # data= [{}, {}]  =====   data={"newses": []} 尤其注意
    return json_status.result(data={"newses": serializer.data})


def news_detail(request, news_id):
    try:
        # /xx/news_id
        # request.GET.get('news_id') # ?news_id=xx
        # news = News.objects.filter(id=news_id, is_delete=False).first() # 不会 会返回None
        news = News.objects.get(id=news_id)  # 如果获取不到的
        # apps.news.models.News.DoesNotExist: News matching query does not exist.
        comments = news.comments.all()  # for comment in comments:  {{ comment.author.username }}
        # return render(request, 'news/news_detail.html', context={"news": news, "comments": comments})
        return render(request, 'news/news_detail.html', context={"news": news})
    except News.DoesNotExist:
        # 抛出 404 错误 就会 去找 404 页面
        raise Http404


@method_decorator([csrf_exempt, ajax_login_required], name="dispatch")
class AddNewsCommentView(View):
    def post(self, request):
        # if request.user.is_authenticated:
        form = AddNewsCommentFrom(request.POST)
        if form.is_valid():
            news_id = form.cleaned_data.get('news_id')
            content = form.cleaned_data.get('content')
            # print(news_id, content)
            news = News.objects.filter(id=news_id).first()
            if news:
                # request.user 匿名用户 必须要登录才能访问这个视图 ajax 方式
                comment = NewsComment.objects.create(content=content, author=request.user, news=news)
                # create 会返回一个对象
                # [Query Set  NewsComment object (8), NewsComment object (7),NewsComment object (6)]
                print(comment)
                print(type(comment))
                # 序列化 不需要加 many=True
                serializer = NewsCommentSerializer(comment)
                print('=======')
                # {'content': '123213123123123321', 'create_time': '2018-10-22T21:43:15.601645+08:00', 'author': OrderedDict([('id', 1), ('username', 'Admin')])}
                print(serializer.data)
                print('=======')
                return json_status.result(data=serializer.data)
            return json_status.params_error(message="新闻不存在")
        return json_status.params_error(message=form.get_error())
        # return json_status.un_auth_error(message="请先登录")


# 后台返回 json 格式数据  前端拿到之后 遍历  restful
def comment_list_with_news(request):
    # 100条 不可能说全部返回 根据新闻id 返回对应的评论
    news_id = request.GET.get("news_id")
    news = News.objects.filter(id=news_id).first()
    if news:
        # 获取当前新闻下的所有 news_comments 是什么类型  QuerySet
        news_comments = news.comments.all()
        # <QuerySet [<NewsComment: NewsComment object (1)>, <NewsComment: NewsComment object (2)>]>
        # {"id": 1,}   [{}, {}, {}]
        # print(news_comments)
        # <QuerySet [{'id': 1, 'content': '这是新闻id为3的 第一条评论', 'create_time': datetime.datetime(2018, 10, 22, 12, 57, 48, 745035, tzinfo=<UTC>), 'author_id': 1, 'news_id': 3}, {'id': 2, 'content': 'news_id=3 第二条评论', 'create_time': datetime.datetime(2018, 10, 22, 12, 59, 17, 857235, tzinfo=<UTC>), 'author_id': 1, 'news_id': 3}]>
        # [{id:1}, {id:2}]
        # .values() 确实可以序列化 一般适合单表
        # {'id': 1, 'content': '这是新闻id为3的 第一条评论', 'create_time': datetime.datetime(2018, 10, 22, 12, 57, 48, 745035, tzinfo=<UTC>), 'author_id': {id:1, username:"which"}, 'news_id': 3} 返回合适的json数据
        # comments = list(news_comments.values())  # QuerySet
        # for comment in comments:
        #     # author_id = comment["author_id"]
        #     # User.objects.filter(id=author_id) # 全部查出来 但是返回的全部字段
        #     print(comment)
        # 两个及以上 必须加参数 many=True xxx 没有属性  filter many=True / get()/ first()/create()
        serializer = NewsCommentSerializer(news_comments, many=True)
        print(serializer)
        print(type(serializer))
        print(dir(serializer))
        return json_status.result(data=serializer.data)
    return json_status.params_error(message="新闻找不到")


def search(request):
    """搜索"""
    # 假如说没有 q 给一个默认值 '' ==  None 到了前端 就是 None
    q = request.GET.get('q', '')
    if q:
        # Q
        ret_newses = News.objects.filter(Q(title__icontains=q)|Q(content__icontains=q)|Q(author__username__icontains=q))
        context = {
            "ret_newses": ret_newses,
            "q": q,
        }
    else:
        hot_newses= NewsHot.objects.filter(is_delete=False).all()
        context = {
            "hot_newses": hot_newses
        }
    return render(request, 'news/search.html', context=context)


# 用于返回 新闻标签的 api 接口  /news/tag/list/
# [{}, {}]  == 返回json 数据  // 接受请求 处理
def news_tag_list(request):

    # 要返回所以的新闻  因为我的代码已经改了 False 表示没有删
    news_tags = NewsTag.objects.filter(is_delete=False).all()
    serializer = NewsTagSerializer(news_tags, many=True)
    return json_status.result(data={"tags": serializer.data})


# 根据 tag_id 返回对应 标签id 下面的新闻 /news/news-with-tag/
def news_with_tag(request):
    # 获取 tag_id
    tag_id = int(request.GET.get('tag_id', 0))
    #
    if tag_id:
        newses = News.objects.filter(is_delete=False, tag=tag_id)
        if not newses:
            return json_status.params_error(message="该分类下无新闻")
    else:
        newses = News.objects.filter(is_delete=False)
    print('======')
    print(newses)
    print('======')
    # 除非是创建 否则基本上都是 many=True
    serializer = NewsSerializer(newses, many=True)
    return json_status.result(data={"newses": serializer.data})


# /api/v1/news/hot/list   # api.域名.com/news/list
# 返回全部热门新闻  /news/hot/list/
def hot_news_list(request):
    # 查出所有没有被删的热门新闻
    hot_newses = NewsHot.objects.filter(is_delete=False)
    serializer = NewsHotSerializer(hot_newses, many=True)
    return json_status.result(data=serializer.data)


# 表示 这个 视图只能接受get 请求 post请求 接收不到
@require_GET   #  /news/banner/list/
def news_banner_list(request):
    """返回banner的列表 """
    # 获取所有的banner
    banners = NewsBanner.objects.filter(is_delete=False)
    # banner 序列化
    serializer = NewsBannerSerializer(banners, many=True)
    # 返回结果 data = {"banners": [{}, {}]}
    return json_status.result(data={"banners": serializer.data})
