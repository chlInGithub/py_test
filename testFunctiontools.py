"""
functools 提供了一些功能，例如lru缓存
"""
from functools import lru_cache


@lru_cache(maxsize=32)
def get_fibonacci_number(n):
    if n < 2:
        return n
    return get_fibonacci_number(n - 1) + get_fibonacci_number(n - 2)


print(get_fibonacci_number(10))  # 输出: 55
