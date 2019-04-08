import memcache
# 建立连接 mem cache 也支持分布式
mc = memcache.Client(['127.0.0.1:11211'])

# 设置
# mc.set(key='username', val='www', time=60)
# mc.set(key='username', val='www', time=60)
# mc.set(key='username', val='www', time=60)
# mc.set(key='username', val='www', time=60)
# None
# print(mc.get('username'))
# print(mc.delete('username'))
# print(mc.get('username'))
# mc.flush_all()
