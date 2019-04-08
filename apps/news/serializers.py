from rest_framework import serializers
from .models import NewsComment, News, NewsTag, NewsHot, NewsBanner
from apps.account.serailizers import UserSerializer


# forms.ModelsFrom serializers.ModelSerializer 后台返回json数据
class NewsCommentSerializer(serializers.ModelSerializer):
    # 相当于 author 序列化
    author = UserSerializer()

    class Meta:
        # 指定序列模型 要序列化的模型
        model = NewsComment
        # 要把模型字段序列化
        # fields = '__all__' 作者 作者 也是一个外键 author_id
        fields = ('content', 'create_time', 'author')


class NewsTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsTag
        fields = ('id', 'name')


class NewsSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    tag = NewsTagSerializer()

    class Meta:
        model = News
        # (), [] 对象.不存在  === undefined
        fields = ('id', 'title', 'desc', 'thumbnail_url', 'pub_time', 'author', 'tag')


class NewsHotSerializer(serializers.ModelSerializer):
    news = NewsSerializer()

    class Meta:
        model = NewsHot
        # fields 里面的字段必须是 model 有的 外键也是一样必须是要存的
        fields = ('id', 'priority', 'is_delete', 'news')


class NewsBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsBanner
        fields = '__all__'

