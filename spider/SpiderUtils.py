import datetime
import socket

import pyautogui
import pymysql
import pyperclip
import redis

from properties import RedisProperties, DBProperties


def get_ip_address():
    try:
        # 创建一个socket对象
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 不需要真正连接到一个远程服务器，只需设置一个远程地址即可
        s.connect(("8.8.8.8", 80))
        # 获取本地端（即本机）的IP地址
        ip_address = s.getsockname()[0]
    finally:
        # 关闭socket连接
        s.close()

    return ip_address


def paste_text(text):
    """将文本复制到剪贴板并粘贴到当前激活窗口"""
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')


def connect_to_database():
    """连接到数据库"""
    return pymysql.connect(
        host=DBProperties.host,
        port=DBProperties.port,
        user=DBProperties.user,
        password=DBProperties.password,
        database=DBProperties.database,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )


def gen_redis():
    return redis.Redis(host=RedisProperties.host, port=RedisProperties.port,
                       password=RedisProperties.password, db=RedisProperties.db)


def calculate_wait_seconds():
    """计算从现在到第二天09:10的秒数"""
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    target_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 9, 10)
    wait_seconds = int((target_time - now).total_seconds())
    print(f'下次时间{target_time} 等待{wait_seconds}秒')
    return wait_seconds
