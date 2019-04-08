import memcache
# 建立连接 mem cache 也支持分布式
mc = memcache.Client(['127.0.0.1:11211'])


# 封装几个方法 设置 / 获取 / 删除  key唯一 set  set_key('username', 'which', time=120)
# key val time
def set_key(key=None, val=None, time=60*5):
    if key and val:
        mc.set(key=key, val=val, time=time)
        return True
    return False


# 获取
def get_key(key=None):
    if key:
        return mc.get(key)
    # 函数默认 返回 None key
    return None


# 删除成功 返回 True 失败 返回 False
def del_key(key=None):
    if key:
        mc.delete(key)
        return True
    return False


# set_key('username', 'Which')
# print(get_key('username'))
# del_key('username')
# print(get_key('username'))
