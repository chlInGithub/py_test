"""
重现类 抽象行为，要求子类必须实现抽象类、抽象类不可实例化。
"""

from abc import ABC, abstractmethod


class MyAbstractClass(ABC):

    @abstractmethod
    def do_something(self):
        pass


class ConcreteClass(MyAbstractClass):
    def do_something(self):
        print("Doing something in the Concrete Class.")


# 实例化抽象基类会引发错误，只能实例化具体实现。
concrete = ConcreteClass()
concrete.do_something()
