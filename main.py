from get_data_info import get_project_info
from flask import Flask, request
from send_msg import dingtalk
from loguru import logger
import hashlib
import config
import json
import hmac

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = (
        "sha256="
        + hmac.new("mykey".encode("utf-8"), request.data, digestmod=hashlib.sha256).hexdigest()
    )

    if hmac.compare_digest(request.headers["X-Signature-256"], signature):
        logger.info(request.data)
        data = json.loads(request.data, encoding="utf-8")
        eventList = config.EVENT_LIST
        if data["event"] == eventList[0]: # 测试 webhook 是否畅通
            username = data['sender']["username"]
            dingtalk(eventList[0], f"@{username} ping cvat webhook successful !")
            logger.info(f"@{username} ping cvat webhook successful !")
            
        if data["event"] == eventList[1]: # 更新项目名字/标签
            pass
        if data["event"] == eventList[2]: # 创建标注任务
            createTaskTime = data["task"]["created_date"]
            taskName = data["task"]["name"] # 任务名字
            taskId = data["task"]["id"] # 任务ID
            taskProId = data["task"]["project_id"] # 项目ID
            create_task_owner = data["task"]["owner"]["username"] # 创建人
            taskdimension = data["task"]["dimension"] # 任务类型：2D 、3D

            ding_data = {
                "createTaskTime": createTaskTime,
                "taskName": taskName,
                "taskId": taskId,
                "create_task_owner": create_task_owner,
                "taskdimension": taskdimension,
                "task_in_project_name": get_project_info(taskProId)
            }

            dingtalk(eventList[2], ding_data)
            
        if data["event"] == eventList[3]: # 更新标注任务状态
            pass
        if data["event"] == eventList[4]: # 删除标注任务
            del_task_owner = data["task"]["owner"]["username"]
            del_task_status = data["task"]["status"]
            del_task_id = data["task"]["id"]
            del_task_name = data["task"]["name"]
            del_task_ProName = get_project_info(data["task"]["project_id"])
            del_task_dimension = data["task"]["dimension"]
            ding_data = {
                "del_task_owner": del_task_owner,
                "del_task_status": del_task_status,
                "del_task_id": del_task_id,
                "del_task_name": del_task_name,
                "del_task_ProName": del_task_ProName,
                "del_task_dimension": del_task_dimension,
            }

            dingtalk(eventList[4], ding_data)

        if data["event"] == eventList[5]: # 创建批注
            pass
        if data["event"] == eventList[6]: # 批注回复
            pass
        if data["event"] == eventList[7]: # 删除批注
            pass
        if data["event"] == eventList[8]: # 批注解决
            pass
        
        return app.response_class(status=200)
    else:
        dingtalk("error", "")
        return app.response_class(status=404)




app.run(host=config.APP_HOST,port=config.APP_PORT, debug=config.APP_DEBUG)

'''
update:job
    '{
        "event": "update:job", 
        "job": {
            "url": "http://10.4.10.254:8080/api/jobs/1866", "id": 1866, "task_id": 2008, "project_id": 73, "assignee": null, "dimension": "2d", "bug_tracker": "", "status": "validation", 
            "stage": "validation", "state": "new", "mode": "annotation", "start_frame": 0, "stop_frame": 9, "data_chunk_size": 15, "data_compressed_chunk_type": "imageset", 
            "updated_date": "2023-04-14T04:35:16.532801Z", 
            "issues": {"count": 0, "url": "http://10.4.10.254:8080/api/issues?job_id=1866"}, 
            "labels": {"count": 4, "url": "http://10.4.10.254:8080/api/labels?job_id=1866"}
        }, 
        "before_update": {"stage": "annotation"}, 
        "webhook_id": 3, 
        "sender": {"url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"}
    }'

update:project
    '{
        "event": "update:project", 
        "project": {
            "url": "http://10.4.10.254:8080/api/projects/73", "id": 73, "name": "imgs_test", 
            "owner": {
                "url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"
            }, 
            "assignee": null, "bug_tracker": "", "created_date": "2023-04-14T02:09:35.759234Z", "updated_date": "2023-04-14T04:28:23.384806Z", 
            "status": "annotation", "dimension": "2d", "organization": null, 
            "target_storage": {
                "id": 84, "location": "local", "cloud_storage_id": null
            }, 
            "source_storage": {
                "id": 83, "location": "local", "cloud_storage_id": null
            }, 
            "tasks": {
                "count": 2, "url": "http://10.4.10.254:8080/api/tasks?project_id=73"
            }, 
            "labels": {
                "count": 5, "url": "http://10.4.10.254:8080/api/labels?project_id=73"
            }, 
            "task_subsets": []
        }, 
        "before_update": {
            "labels": {
                "count": 4, "url": "http://10.4.10.254:8080/api/labels?project_id=73"
            }
        }, 
        "webhook_id": 3, 
        "sender": {"url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"}
    }'


create:issue
    '{
        "event": "create:issue", 
        "issue": {
            "id": 192, "frame": 0, "position": [327.423828125, 690.265625, 327.423828125, 693.6064453125], "job": 1866, 
            "owner": {
                "url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"
            }, 
            "assignee": null, "created_date": "2023-04-14T05:47:16.347717Z", "updated_date": null, "resolved": false, 
            "comments": {
                "count": 1, "url": "http://10.4.10.254:8080/api/comments?issue_id=192"
            }
        }, 
        "webhook_id": 3, 
        "sender": {"url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"}
    }'

create:comment
    '{
        "event": "create:comment", 
        "comment": {
            "id": 227, "issue": 192, 
            "owner": {"url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"}, 
            "message": "ff", "created_date": "2023-04-14T06:40:40.606739Z", "updated_date": "2023-04-14T06:40:40.606765Z"
        }, 
        "webhook_id": 3, 
        "sender": {"url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"}
    }'

delete:issue
    '{
        "event": "delete:issue", 
        "issue": {
            "id": 191, "frame": 0, "position": [316.53125, 711.8173828125, 316.53125, 715.98828125], "job": 1866, 
            "owner": {
                "url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"
            }, 
            "assignee": null, "created_date": "2023-04-14T05:08:53.913378Z", "updated_date": null, "resolved": false, 
            "comments": {
                "count": 1, "url": "http://10.4.10.254:8080/api/comments?issue_id=191"
            }
        }, 
        "webhook_id": 3, 
        "sender": {"url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"}
    }'

update:issue
    '{
        "event": "update:issue", 
        "issue": {
            "id": 192, "frame": 0, "position": [327.423828125, 690.265625, 327.423828125, 693.6064453125], "job": 1866, 
            "owner": {
                "url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"
            }, 
            "assignee": null, "created_date": "2023-04-14T05:47:16.347717Z", "updated_date": null, "resolved": true, 
            "comments": {
                "count": 1, "url": "http://10.4.10.254:8080/api/comments?issue_id=192"
            }
        }, 
        "before_update": {"resolved": false}, "webhook_id": 3, 
        "sender": {"url": "http://10.4.10.254:8080/api/users/1", "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"}
    }'    

'''