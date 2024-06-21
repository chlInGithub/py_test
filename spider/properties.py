"""
配置信息
"""

__all__ = ['RedisProperties', 'DBProperties', 'MitmproxyProperties', 'SpiderProperties']


class RedisProperties:
    host = 'xxx'
    port = 6379
    password = 'xxx'
    db = 8


class DBProperties:
    host = 'xxx'
    port = 3306
    user = 'xxx'
    password = 'xxx'
    database = 'xx'


class MitmproxyProperties:
    focus_host = "xx"


class SpiderProperties:
    jxxs_name = 'xxx'
