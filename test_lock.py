"""
threading.Look 是一个基本的同步原语，用于确保某段代码在同一时间只被一个线程执行。
threading.RLock 重入锁

multiprocessing.Lock 多进程之间的同步锁
"""

import threading
import time


class TestThreadingLock:
    threading_lock = threading.Lock()
    shared_count = 0

    @staticmethod
    def incr():
        for i in range(10000):
            # with 做了获取锁，释放锁
            with TestThreadingLock.threading_lock:
                o = TestThreadingLock.shared_count
                TestThreadingLock.shared_count += 1
                assert [TestThreadingLock.shared_count, o+1]
                print(f'{o} + 1 = {TestThreadingLock.shared_count}')

    @staticmethod
    def decr():
        for i in range(10000):
            with TestThreadingLock.threading_lock:
                o = TestThreadingLock.shared_count
                TestThreadingLock.shared_count -= 1
                assert [TestThreadingLock.shared_count, o - 1]
                print(f'{o} - 1 = {TestThreadingLock.shared_count}')


def test_threading_lock():
    thread_incr = threading.Thread(target=TestThreadingLock.incr)
    thread_decr = threading.Thread(target=TestThreadingLock.decr)

    thread_incr.start()
    thread_decr.start()

    thread_incr.join()
    thread_decr.join()


if __name__ == '__main__':
    test_threading_lock()
