"""
mitmproxy 工具类，提供开启和关系mitmproxy的静态方法
"""
import datetime
import subprocess
import time

import requests

from net_proxy_utils import NetProxyUtils

__all__ = ['MitmproxyUtils']


class MitmproxyUtils:
    # 定义静态变量
    mitmproxy_addon_file_path: str = None
    mitmproxy_log_file_path: str = None
    log_file = None
    process: subprocess.Popen = None

    @staticmethod
    def run_mitmproxy():
        server = '127.0.0.1'
        port = '9999'
        if MitmproxyUtils.mitmproxy_addon_file_path is None or MitmproxyUtils.mitmproxy_log_file_path is None:
            print("must need mitmproxy_addon_file_path")
            raise Exception('must need mitmproxy_addon_file_path')
        log_file_name = MitmproxyUtils.mitmproxy_log_file_path + datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        print(f"log_file_name is {log_file_name}")
        MitmproxyUtils.log_file = open(log_file_name, "x")
        mitmproxy_command = ["mitmdump", "-p", port, "-s", MitmproxyUtils.mitmproxy_addon_file_path]
        process = subprocess.Popen(mitmproxy_command, stdout=MitmproxyUtils.log_file, stderr=MitmproxyUtils.log_file,
                                   text=True)
        MitmproxyUtils.process = process

        if NetProxyUtils.enable_proxy(server, port) is False:
            raise Exception(f'set proxy fail ：{server} {port}')

        wait_s = 5
        time.sleep(wait_s)
        print(f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")} 已经等待{wait_s}s')

        boot_success = False
        # 等待 mitmproxy 启动成功
        with open(log_file_name, "r") as log_file:
            for i in range(0, 20):
                try:
                    print(f'http response status {requests.get("http://www.baidu.com").status_code}')
                except IOError as e:
                    print(f'mitmproxy 还没有起来 或 检查端口是否一致 {e}')
                output = log_file.readline()
                if output == '' and process.poll() is not None:
                    break
                if 'listening at' in output:
                    print("Mitmproxy started successfully.")
                    boot_success = True
                    break

                time.sleep(2)  # 避免过于频繁地读取输出
                wait_s += 2
                print(f'{datetime.datetime.now().strftime("%Y%m%d%H%M%S")} 已经等待{wait_s}s')

        # 检查 mitmproxy 是否启动失败
        if boot_success is False or (process.poll() is not None and process.returncode != 0):
            print(f"Mitmproxy failed to start.{process.returncode}")
            raise Exception('Mitmproxy failed to start')

        print("Mitmproxy success to start.")

    @staticmethod
    def exit_mitmproxy():
        NetProxyUtils.disable_proxy()

        if MitmproxyUtils.process:
            # 确保在所有操作完成后关闭 mitmproxy 进程
            print("Shutting down mitmproxy...")
            process = MitmproxyUtils.process
            MitmproxyUtils.process = None
            process.terminate()

        if MitmproxyUtils.log_file:
            log_file = MitmproxyUtils.log_file
            MitmproxyUtils.log_file = None
            log_file.close()
