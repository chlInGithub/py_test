class Person():
    # 这里定义的都是静态成员
    name: str = None
    age: int = None

    def __init__(self, name, age):
        # self. 定义的是实例成员，建议在__init__里面定义
        self.name = name
        self.age = age
        self.name_2 = None

    def gen_name_2(self):
        self.name_2 = self.name + '的第二个名字'


if __name__ == '__main__':
    person_a = Person('A', 10)
    person_a.gen_name_2()
    Person.name = 'staticA'
    Person.age = 20
    person_b = Person('B', 30)
    person_b.gen_name_2()
    Person.name = 'staticB'
    person_c = Person('C', 40)
    person_c.gen_name_2()
    print(f'person_a {person_a.name} {person_a.age} {person_a.name_2}, {Person.name} {Person.age}')
    print(f'person_b {person_b.name} {person_b.age} {person_a.name_2}, {Person.name} {Person.age}')
    print(f'person_c {person_c.name} {person_c.age} {person_a.name_2}, {Person.name} {Person.age}')