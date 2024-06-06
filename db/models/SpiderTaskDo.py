"""
数据模型
"""

from sqlalchemy import Column, String, Integer, BigInteger
from . import Base
# 数据模型对象序列化 提供了to_dict()的实现 子类对象可转为字典形式
from sqlalchemy_serializer import SerializerMixin


class SpiderTaskDo(Base, SerializerMixin):
    __tablename__ = 't_spider_task'
    id = Column(BigInteger, primary_key=True)
    task_type = Column(String(128))
    params = Column(String(128))
    user_params = Column(String(128))
    clause_cid = Column(String(255))
