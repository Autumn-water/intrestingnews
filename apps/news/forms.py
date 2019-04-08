from django import forms
from apps.forms import FormMixin


class AddNewsCommentFrom(forms.Form, FormMixin):
    news_id = forms.IntegerField(error_messages={"required": "新闻id错误"})
    content = forms.CharField(error_messages={"required": "新闻评论不能为空"})
