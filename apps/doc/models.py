from django.db import models


class Doc(models.Model):
    # 文件路径
    file_path = models.URLField()
    # 文档标题
    title = models.CharField(max_length=50)
    # 描述信息
    desc = models.CharField(max_length=200)
    # 创建日期
    create_date = models.DateTimeField(auto_now_add=True)
    # 是否删除
    is_delete = models.BooleanField(default=False)
    # 上传用户
    author = models.ForeignKey('account.User', on_delete=models.CASCADE, blank=True)
