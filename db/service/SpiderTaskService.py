"""
spiderTask服务
"""

import logging

from db.database import Session
from db.models.SpiderTaskDo import SpiderTaskDo
from sqlalchemy import text


def selectByTaskType(task_type: str, page_index: int, page_size: int) -> list[SpiderTaskDo]:
    """
不需要人为编写sql
    @param task_type:
    @param page_index:
    @param page_size:
    @return:
    """
    session = Session()
    try:
        return session.query(SpiderTaskDo).filter(SpiderTaskDo.task_type == task_type).offset(
            (page_index - 1) * page_size).limit(page_size).all()
    finally:
        session.close()


def selectViaSqlByTaskType(task_type: str, page_index: int, page_size: int) -> list[SpiderTaskDo]:
    """
需人为编写sql语句
    @param task_type:
    @param page_index:
    @param page_size:
    @return:
    """
    session = Session()
    try:
        # 限制：要求 select 的结果字段 必须 在数据模型中，否则报错。
        temp_items = session.execute(text('select id,task_type, params,user_params,clause_cid from t_spider_task where task_type = :task_type order by id desc limit :offset, :page_size'), {'task_type':task_type, 'offset':(page_index - 1) * page_size, 'page_size': page_size}).fetchall()
        items = [SpiderTaskDo(**dict(temp_item._mapping)) for temp_item in temp_items]
        return items
    finally:
        session.close()
