import redis
import pyautogui
import pyperclip
import time
import pymysql
import socket
import datetime
import random
import traceback
import os

def paste_text(text):
    """将文本复制到剪贴板并粘贴到当前激活窗口"""
    pyperclip.copy(text)
    pyautogui.hotkey('ctrl', 'v')


def click_button(image_path):
    """点击屏幕上与给定图片匹配的按钮"""
    button_location = pyautogui.locateOnScreen(image_path)
    if button_location:
        button_center = pyautogui.center(button_location)
        pyautogui.click(button_center)
        return True
    else:
        print(f"未找到匹配的按钮: {image_path}")
        return False

def double_click_button(image_path):
    """点击屏幕上与给定图片匹配的按钮"""
    button_location = pyautogui.locateOnScreen(image_path)
    if button_location:
        button_center = pyautogui.center(button_location)
        pyautogui.doubleClick(button_center)
        return True
    else:
        print(f"未找到匹配的按钮: {image_path}")
        return False

def query_task_by_id(connection, id):
    """根据ID查询一条数据"""
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM t_spider_task WHERE id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Query task error: {e}")


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

def calculate_wait_seconds():
    """计算从现在到第二天00:10的秒数"""
    now = datetime.datetime.now()
    tomorrow = now + datetime.timedelta(days=1)
    target_time = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day, 9, 10)
    wait_seconds = (target_time - now).total_seconds()
    return wait_seconds


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_dir = os.path.join(current_dir, 'img')
    clauseName = '复星保德信星海赢家（龙腾版）养老年金保险'

    print(f"处理任务元素: {clauseName}")

    # 点击输入框位置，并输入内容（假设input_box.png是输入框的截图）
    pyautogui.doubleClick(46, 48)
    time.sleep(1)
    # 微信搜索框
    pyautogui.click(587, 48)
    time.sleep(1)
    paste_text('公众号名称')
    time.sleep(2)
    # 搜索结果
    pyautogui.click(590, 119)
    time.sleep(1)
    # 公众号窗口 条款按钮
    pyautogui.click(873, 612)
    time.sleep(1)
    # 保险搜索按钮
    pyautogui.click(856, 511)
    time.sleep(10)
    # jxxs 搜索框
    pyautogui.click(160, 74)
    paste_text(clauseName)
    time.sleep(1)
    # 搜素按钮
    pyautogui.click(1336, 66)
    time.sleep(5)
    # 关闭浏览器
    pyautogui.click(1343, 15)

if __name__ == '__main__':
    main()
