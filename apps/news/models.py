from django.db import models


#  ORM(objects  Relet  manage)对象关系映射
# 设计模型 Django w帮助 模型 映射成数据库
class NewsTag(models.Model):
    # 字段
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    # 字段 用于标识是否删除  False
    # 假删 （ python 判断 逻辑删除） update(is_delete=True) / 真删（物理删除） delete()
    is_delete = models.BooleanField(default=False)


# 新闻模型
class News(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    # 不是真正存图片 存图片 url 地址
    thumbnail_url = models.URLField()
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    # 外键 标签 作者 CASCADE 级联删除(只是在真删才有效果) 以前 硬盘普遍小（普通数据真删）
    tag = models.ForeignKey('NewsTag', on_delete=models.CASCADE)
    author = models.ForeignKey('account.User', on_delete=models.CASCADE)

    class Meta:
        # (, ) [] 倒序 -id  默认的顺序
        # 全是倒序
        ordering = ['-id']


class NewsComment(models.Model):
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

    # 谁 评论所属的新闻
    author = models.ForeignKey('account.User', on_delete=models.CASCADE)
    # related_name 反向名字 通过新闻找评论 comment_set
    news = models.ForeignKey('News', on_delete=models.CASCADE, related_name='comments')

    class Meta:
        # (, ) [] 倒序 -id  默认的顺序
        # 全是倒序
        ordering = ['-id']


class NewsHot(models.Model):
    # 一对一
    news = models.OneToOneField('News', on_delete=models.CASCADE)
    # 优先级
    priority = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        # 默认是从小到大  - (取反)
        ordering = ['-priority']


class NewsBanner(models.Model):
    """新闻轮播图"""
    image_url = models.URLField()
    priority = models.IntegerField()
    # 就和 emailField 帮助我们 验证数据是不是 url 格式的
    link_to = models.URLField()
    create_date = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-priority']
