"""
封装通用的insert、get_by_id、updateById
"""

from db.database import Session


def insert(instances:list):
    """

    @param instances: 数据模型实例列表
    """
    session = Session()
    try:
        session.bulk_save_objects(instances)
        session.commit()
    finally:
        session.close()

def get_by_id(clazz, id: int):
    """

    @param clazz： 指定模型class
    @param id： 记录ID
    @return： 对应clazz的实例
    """
    session = Session()
    try:
        return session.query(clazz).filter(clazz.id == id).first()
    finally:
        session.close()


def updateById(clazz, instance) -> bool:
    """

    @param clazz: 指定模型class
    @param instance: clazz实例并赋值需更新数据，必须有id
    @return: True成功
    """
    if instance.id is None:
        return False
    temp_dict: dict = instance.to_dict()
    update_dict: dict = temp_dict.copy()
    keys = temp_dict.keys()
    for key in keys:
        if temp_dict.get(key) is None:
            update_dict.pop(key)
    if len(update_dict) < 2:
        print('参数数量小于2')
        return False

    session = Session()
    try:
        # dict中所有字段都会出现在update语句中，即使数据是None
        count = session.query(clazz).filter(clazz.id == instance.id).update(update_dict)
        print(f'update count {count}')
        session.commit()
        return count > 0
    finally:
        session.close()

