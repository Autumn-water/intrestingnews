from django import template
from django.utils.timezone import now
from datetime import datetime

# 生成一个注册
register = template.Library()


@register.filter
def date_format(val):
    # 判断一下 是不是时间日期类型
    if not isinstance(val, datetime):
        return val
    # 获取此刻时间
    time_now = now()
    # 新闻发布时间  val 当前时间减去新闻发布时间 得到间隔秒
    sec = (time_now-val).total_seconds()

    # 把秒转为 刚刚 几分钟 几小时前
    if sec < 60:
        return '刚刚'
    # sec >= 60 and sec < 60*60
    elif 60 <= sec < 60*60:
        mint = int(sec / 60)
        return '{}分钟前'.format(mint)
    elif 60*60 <= sec < 60*60*24:
        hour = int(sec / 60 / 60)
        return '{}小时前'.format(hour)
    elif 60*60*24 <= sec < 60*60*24*2:
        return '昨天'
    else:
        return val.strftime('%m/%d %H:%M')

