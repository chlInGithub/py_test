"""
py默认不进行类型检查，所以虽然变量A定义为int类型，但是可以为其赋值字符串。
如下实现强制类型检查
"""

from dataclasses import dataclass


class TypedProperty:
    def __init__(self, name, type):
        self.name = "_" + name
        self.type = type

    def __get__(self, instance, cls):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        if not isinstance(value, self.type):
            raise TypeError(f"Value must be {self.type}")
        setattr(instance, self.name, value)


class Person:
    name = TypedProperty("name", str)
    age = TypedProperty("age", int)


@dataclass
class Person1:
    name: str
    age: int

    def __repr__(self):
        return f'name {self.name} age {self.age}'


p = Person()
p.name = "Alice"
p.age = 30
print(Person1('test', '1'))
print(p.name, p.age)
