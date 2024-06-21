from functools import reduce
list = range(1,20)
# 直接生成了一个新的list
list1 = [x for x in list if x % 2 == 0]
# 对序列元素，从左到右使用两元函数进行合并。例如所有元素的乘积
list2 = reduce(lambda x, y: x*y, list1)
# 得到一个生成器generator
list3 = (x for x in list if x % 2 == 0)
for x in list:
    print(x)
print(list1)
print(list2)
for x in list3:
    print(x)

print("1+2+3+4=",reduce(lambda x,y:x+y, range(1,5)))
print("1*2*3*4=",reduce(lambda x,y:x*y, range(1,5)))
