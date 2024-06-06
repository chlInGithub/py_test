"""
自定义行为：通过类实例‘读取’不存在的属性时如何处理。
默认情况抛出AttributeError，表示读取的属性不存在。

"""


class Return_type:
    pass

class DynamicAttributes:
    def __getattr__(self, item) -> str:
        return f"You are trying to access {item}, which does not exist!"
    def test(self, p:int) -> str:
        return f'p is {p}'

d = DynamicAttributes()

print(d.test('uds'))

d.some_random_attribute1 = '1'
print('some_random_attribute1 : ' + d.some_random_attribute1)
a= d.some_random_attribute
print(d.some_random_attribute)
