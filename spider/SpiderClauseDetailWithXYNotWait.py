import datetime
import random
import time
import traceback

import pyautogui

import SpiderUtils


class DBException(Exception):
    pass


def query_task_by_id(connection, id):
    """根据ID查询一条数据"""
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM t_spider_task WHERE id = %s"
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(f"Query task {id} error: {e}")
        raise DBException(e)


def spider():
    # 连接到Redis服务器（根据你的Redis配置进行修改）
    r = SpiderUtils.gen_redis()
    conn = SpiderUtils.connect_to_database()
    test = 0
    task_list_key = 'spider:task_id_list:clauseDetailByPerson'
    task_ip_date_counter_key = 'spider:task_ip_date_counter'
    task_clause_list_item_count_key = 'spider:task_clause_list_item_count'
    task_clause_list_item_has_tags_key = 'spider:task_clause_list_item_has_tags'
    ip_address = SpiderUtils.get_ip_address()
    max_count = 300
    has_res_error = 0
    res_error = ''
    res_error_count = 0
    while True:
        today_str = datetime.datetime.now().strftime("%Y%m%d")
        temp_hour = datetime.datetime.now().hour
        if temp_hour < 9 or temp_hour > 21:
            print(f'{today_str} 不在9-21点之间，等待30分钟')
            time.sleep(60 * 30)

        field_search = f"{ip_address}_{today_str}_clauseSearch"
        field_detail = f"{ip_address}_{today_str}_clauseDetailByPerson"
        ip_date_count = r.hget(task_ip_date_counter_key, field_detail)
        if ip_date_count is not None and int(ip_date_count) > max_count:
            # 等待知道第二天0点10分
            print(f"{today_str} 今天次数已用完  已使用{ip_date_count}")
            break

        if has_res_error is not None and has_res_error == 1:
            if res_error_count <= 3:
                print(f'{today_str} 接口第{res_error_count}次返回错误信息')
                time.sleep(60)
            else:
                has_res_error = 0
                res_error_count = 0
                # 等待知道第二天0点10分
                print(f"{today_str} 今天数次接口返回错误信息 等待到第二天 {res_error}")
                break

        # 从名为'queue_name'的阻塞队列中获取元素，超时时间设置为None表示无限等待直到获取到元素
        try:
            _, task_id = r.brpop(task_list_key, timeout=None)
        except Exception as e:
            r = SpiderUtils.gen_redis()

        # 由于任务队列中放的是字符串
        task_id = int(task_id.decode('utf-8').strip('"'))
        spider_task = query_task_by_id(conn, task_id)

        has_in_jxxs = 0

        try:
            if spider_task:
                task_type = spider_task['task_type']
                if 'clauseDetailByPerson' == task_type:
                    params = spider_task['params']
                    if params:
                        clauseName = params
                        # clauseName = '复星保德信星海赢家（龙腾版）养老年金保险'

                        print(f"{today_str} 处理任务元素: {clauseName}")

                        # 双击微信桌面快捷方式
                        pyautogui.doubleClick(46, 48)
                        time.sleep(1)
                        # 微信搜索框
                        pyautogui.click(587, 48)
                        time.sleep(1)
                        SpiderUtils.paste_text('公众号名称')
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
                        has_in_jxxs = 1
                        SpiderUtils.paste_text(clauseName)
                        time.sleep(1)
                        # 搜素按钮
                        pyautogui.click(1336, 66)
                        time.sleep(5)
                        r.hincrby(task_ip_date_counter_key, field_search, 1)

                        res_error = r.hget('spider:ip_error', ip_address)
                        if res_error:
                            print(f'has_res_error detail {res_error}')
                            has_res_error = 1
                            r.hdel('spider:ip_error', ip_address)
                            res_error_count = res_error_count + 1
                            raise Exception('has_res_error detail')

                        # 避免浪费次数
                        if 1 == test:
                            r.lpush(task_list_key, task_id)
                            continue
                        else:
                            # Point(x=1315, y=278)
                            # 循环点击每个“原文文档”按钮（假设document_button.png是“原文文档”按钮的截图）
                            # 有标签时右边第一个坐标
                            x = 1315
                            y = 270
                            y_interval = 170
                            task_clause_list_item_has_tags = r.hget(task_clause_list_item_has_tags_key, ip_address)
                            # 无标签
                            if task_clause_list_item_has_tags is None or int(task_clause_list_item_has_tags) < 1:
                                y = 260
                                y_interval = 150
                            task_clause_list_item_count = r.hget(task_clause_list_item_count_key, ip_address)
                            if task_clause_list_item_count is not None and int(task_clause_list_item_count) > 0:
                                if int(task_clause_list_item_count) > 3:
                                    task_clause_list_item_count = 3
                                for i in range(int(task_clause_list_item_count)):
                                    pyautogui.click(x, y + y_interval * i)
                                    time.sleep(5)

                                    r.hincrby(task_ip_date_counter_key, field_detail, 1)

                                    res_error = r.hget('spider:ip_error', ip_address)
                                    if res_error:
                                        print(f'has_res_error detail {res_error}')
                                        has_res_error = 1
                                        r.hdel('spider:ip_error', ip_address)
                                        res_error_count = res_error_count + 1
                                        raise Exception('has_res_error detail')

                                    # 点击回退
                                    pyautogui.click(19, 16)
                                    time.sleep(3)
                            r.hdel(task_clause_list_item_count_key, ip_address)
                        pyautogui.hotkey('alt', 'f4')
        except Exception as e:
            print(f"{today_str} task deal error: {e}")
            traceback.print_exc()
            try:
                r.lpush(task_list_key, task_id)
            except Exception as e1:
                r = SpiderUtils.gen_redis()

            if has_in_jxxs == 1:
                pyautogui.hotkey('alt', 'f4')
            # 如果数据库异常，则重新建立连接
            if isinstance(e, DBException):
                conn = SpiderUtils.connect_to_database()

        wait_seconds = random.randint(30, 120)
        print(f"{today_str} task deal wait: {wait_seconds} s")
        time.sleep(wait_seconds)
        print(f'{today_str} task deal wait done')
    print("结束条款详情")

if __name__ == '__main__':
    spider()
