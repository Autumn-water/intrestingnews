from django import forms
from apps.forms import FormMixin
from apps.doc.models import Doc


class NewsPubForm(forms.Form, FormMixin):
    title = forms.CharField(max_length=100, min_length=2, error_messages={"required":"新闻标题不能为空", "max_length": "新闻标题最大不能超过100"})
    desc = forms.CharField(max_length=200, min_length=2, error_messages={"required":"新闻描述不能为空"})
    tag_id = forms.IntegerField(error_messages={"required":"不能为空"})
    thumbnail_url = forms.URLField(error_messages={"required":"不能为空"})
    content = forms.CharField(max_length=100000)


class NewsHotAddForm(forms.Form, FormMixin):
    news_id = forms.IntegerField(error_messages={"required":"参数错误"})
    priority = forms.IntegerField(error_messages={"required": "优先级不能为空"})


class NewsEditForm(NewsPubForm):
    news_id = forms.IntegerField(error_messages={'required': "新闻id错误"})


class NewsBannerForm(forms.Form, FormMixin):
    image_url = forms.URLField(error_messages={"required": "图片地址不能为空", "invalid": "请输入合法的网址"})
    priority = forms.IntegerField(error_messages={"required": "优先级不能为空"})
    link_to = forms.URLField(error_messages={"required": "跳转地址不能为空", "invalid": "请输入合法的网址"})


class CoursePubForm(forms.Form, FormMixin):
    category_id = forms.IntegerField(error_messages={"required": "课程id错误"})
    teacher_id = forms.IntegerField(error_messages={"required": "讲师id错误"})
    title = forms.CharField(error_messages={"required": "新闻标题错误"})
    cover_url = forms.URLField(error_messages={"required": "课程封面", "invalid": "课程封面地址不合法"})
    video_url = forms.URLField(error_messages={"required": "课程视频不能为空", "invalid": "视频地址不合法"})
    duration = forms.IntegerField(error_messages={"required": "课程时长不能为空"})
    profile = forms.CharField(error_messages={"required": "课程简介不能为空"})
    outline = forms.CharField(error_messages={"required":"课程大纲不能为空"})


# ModelSerializers
class DocUploadForm(forms.ModelForm, FormMixin):

    """文档上传验证"""
    class Meta:
        # 知道模型
        model = Doc
        # 全部字段
        fields = '__all__'
        # 错误提醒
        error_messages = {
            "file_path": {
                "required": "文件路径不能为空",
                "invalid": "格式错误"
            },
            "title": {
                "required": "文档标题不能为空"
            }
        }
