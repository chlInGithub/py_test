"""
异步编程: asyncio async await
"""
import asyncio
import aiohttp
import time
import threading
from concurrent.futures import ThreadPoolExecutor
import requests


async def fetch_data_async(url):
    """
异步获取数据
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            print(threading.current_thread().name)
            result = await response.text()
            # print('done')
            return result


def fetch_data(url):
    """
同步获取信息
    :param url:
    :return:
    """
    print(threading.current_thread().name)
    response = requests.get(url)
    result = response.text
    # print('done')
    return result


async def main_use_asyncio_with_one_thread():
    # task必须是异步行为，asyncio.create_task多个task，await asyncio.gather等待多个task处理完毕。
    # asyncio是使用当前线程+事件循环的方式达到提高处理多个任务整体效率的目标，需要注意每个任务仍然使用当前线程。
    # 多个IO密集型任务，比串行效率高。
    # 多个cpu密集型任务，无法体现效果。
    # 以下任务均由MainThread执行
    task1 = asyncio.create_task(fetch_data_async('http://www.baidu.com'))
    task2 = asyncio.create_task(fetch_data_async('http://www.baidu.com'))
    task3 = asyncio.create_task(fetch_data_async('http://www.baidu.com'))
    task4 = asyncio.create_task(fetch_data_async('http://www.baidu.com'))
    task5 = asyncio.create_task(fetch_data_async('http://www.baidu.com'))
    task6 = asyncio.create_task(fetch_data_async('http://www.baidu.com'))
    results = await asyncio.gather(*[task1, task2, task3, task4, task5, task6])

    # 等待 task 执行完
    # r1 = results[0]
    # print(f'size {len(r1)}')
    # r2 = results[1]
    # r3 = results[2]
    # r4 = results[3]
    # print(f'size {len(r4)}')
    # r5 = results[4]
    # r6 = results[5]
    # print(f'size {len(r6)}')


async def main_use_asyncio_with_thread_pool():
    """
asyncio + 线程池，task由线程池中线程执行，提升效率效果更明显。
    """
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as thread_pool_executor:
        # 这里调用的func必须是同步行为，否则asyncio会出现找不到event loop问题
        task1 = loop.run_in_executor(thread_pool_executor, fetch_data, 'http://www.baidu.com')
        task2 = loop.run_in_executor(thread_pool_executor, fetch_data, 'http://www.baidu.com')
        task3 = loop.run_in_executor(thread_pool_executor, fetch_data, 'http://www.baidu.com')
        task4 = loop.run_in_executor(thread_pool_executor, fetch_data, 'http://www.baidu.com')
        task5 = loop.run_in_executor(thread_pool_executor, fetch_data, 'http://www.baidu.com')
        task6 = loop.run_in_executor(thread_pool_executor, fetch_data, 'http://www.baidu.com')
        results = await asyncio.gather(*[task1, task2, task3, task4, task5, task6])



async def main_sync():
    """
虽然使用异步关键字，但是执行效果和串行一样
    """
    # 多个task串行执行
    r1 = await fetch_data_async('http://www.baidu.com')
    await fetch_data_async('http://www.baidu.com')
    await fetch_data_async('http://www.baidu.com')
    r4 = await fetch_data_async('http://www.baidu.com')
    await fetch_data_async('http://www.baidu.com')
    r6 = await fetch_data_async('http://www.baidu.com')
    # print(f'size {len(r1)}')
    # print(f'size {len(r4)}')
    # print(f'size {len(r6)}')


start_time = time.time()
asyncio.run(main_use_asyncio_with_one_thread())
end_time = time.time()
print(f"main_use_asyncio_with_one_thread {end_time - start_time} seconds to execute.")


start_time = time.time()
asyncio.run(main_use_asyncio_with_thread_pool())
end_time = time.time()
print(f"main_use_asyncio_with_thread_pool {end_time - start_time} seconds to execute.")

start_time = time.time()
asyncio.run(main_sync())
end_time = time.time()
print(f"main1 {end_time - start_time} seconds to execute.")
