from functools import reduce
list = range(1,20)
list1 = [x for x in list if x % 2 == 0]
list2 = reduce(lambda x, y: x*y, list1)
list3 = (x for x in list if x % 2 == 0)
for x in list:
    print(x)
print(list1)
print(list2)
for x in list3:
    print(x)