"""
装饰器，在方法A外围包裹一层，可在方法A执行前后添加自定义行为。
"""
def decorator1(func):
    def wrapper():
        print("Decorator1")
        func()
    return wrapper

def decorator2(func):
    def wrapper():
        print("Decorator2")
        func()
    return wrapper

def logger(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == 'INFO':
                print(f"[{level}] - {func.__name__} is called")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@decorator1
@decorator2
@logger(level='INFO')
def greet():
    print("Hello")

greet()
