"""
测试异常捕获顺序：
按照expect代码顺序，命中第一个满足条件的expect；
异常父类可匹配其子类；
"""


class AError(IOError):
    pass


class BError(IOError):
    pass


class CError(AError):
    pass


def test():
    try:
        raise BError("xxxxxx")
    except CError as e:
        print(f'cerror {e}')
    except IOError as e:
        print(f'have ex {e}')


test()