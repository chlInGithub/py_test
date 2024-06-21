"""
重现类 抽象行为，要求子类必须实现抽象类、抽象类不可实例化。
"""

from abc import ABC, abstractmethod


class MyAbstractClass(ABC):

    @abstractmethod
    def do_something(self):
        pass


class ConcreteClass(MyAbstractClass):
    # private静态变量
    __static_param:str = None
    # public静态变量
    static_param:str = None
    # protected静态变量
    _static_param:str = None

    # 静态方法
    @staticmethod
    def set_param(param):
        ConcreteClass.__static_param = param

    @staticmethod
    def get_param():
        return ConcreteClass.__static_param

    def do_something(self):
        print("Doing something in the Concrete Class.")


# 实例化抽象基类会引发错误，只能实例化具体实现。
concrete = ConcreteClass()
concrete.do_something()
ConcreteClass.set_param('hello')
print(f'{concrete.get_param()},{ConcreteClass.get_param()}')