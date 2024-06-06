import schedule
import time
import SpiderPDFWithXYNotWait as spiderPdf
import SpiderClauseDetailWithXYNotWait as spiderClauseDetail


def job():
    print("开始JOB")
    spiderPdf.spider()
    spiderClauseDetail.spider()
    print("结束JOB")


# 每天9点10分执行任务
schedule.every().day.at("09:10").do(job)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)
