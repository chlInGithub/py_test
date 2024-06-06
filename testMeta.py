class Meta(type):
    def __init__(cls, name, bases, dct):
        if not hasattr(cls, 'registry'):
            cls.registry = {}
        else:
            cls.registry[name.lower()] = cls
        super().__init__(name, bases, dct)

class Base(metaclass=Meta):
    pass

class A(Base):
    pass

class B(Base):
    pass

print(Base.registry)