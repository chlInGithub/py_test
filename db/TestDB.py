import service.SpiderTaskService as spiderTaskService
import service.CommonService as commonService
from models.SpiderTaskDo import SpiderTaskDo as spiderTaskDo
import json


spiderTask: spiderTaskDo = commonService.get_by_id(spiderTaskDo, 1785150025564778498)
if spiderTask:
    print(f'cid is {spiderTask.clause_cid}')
    print(json.dumps(spiderTask.to_dict()))
    print(spiderTask.to_dict())

# update_task:spiderTaskDo = spiderTaskDo()
# update_task.id = spiderTask.id
# update_task.user_params = 'testUserParams'
# commonService.updateById(spiderTaskDo, update_task)

new_spider_task = spiderTaskDo(task_type='clauseDetailByPerson')
commonService.insert([new_spider_task])

spider_task_list: list[spiderTaskDo] = spiderTaskService.selectViaSqlByTaskType('clauseDetailByPerson', 1, 10)
for spider_task in spider_task_list:
    print(spider_task.to_dict())
