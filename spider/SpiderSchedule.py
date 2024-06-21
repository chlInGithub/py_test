import sys
import time

import schedule

import SpiderClauseDetailWithXYNotWait as spiderClauseDetail
import SpiderPDFWithXYNotWait as spiderPdf
from mitmproxy_utils import MitmproxyUtils


def job():
    try:
        MitmproxyUtils.run_mitmproxy()
        print("开始JOB")
        spiderPdf.spider()
        spiderClauseDetail.spider()
        print("结束JOB")
    finally:
        MitmproxyUtils.exit_mitmproxy()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: python SpiderSchedule.py <mitmproxy_addon_file_path> <mitmproxy_log_file_path> <run_now 1 or 0>")
        sys.exit(1)

    MitmproxyUtils.mitmproxy_addon_file_path = sys.argv[1]
    MitmproxyUtils.mitmproxy_log_file_path = sys.argv[2]
    run_now = sys.argv[3]
    if int(run_now) == 1:
        print("执行一次任务")
        job()

    # 每天9点10分执行任务
    schedule.every().day.at("09:10").do(job)
    print("已经开始定时任务")
    while True:
        schedule.run_pending()
        time.sleep(1)
