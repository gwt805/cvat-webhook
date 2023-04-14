# pip install cvat-sdk -U
from get_data_info import get_task_info, get_project_info
from flask import Flask, request
from send_msg import wb_dingtalk
from loguru import logger
import hashlib
import config
import json
import hmac

# wb_dingtalk(json.dumps(data, indent=2))


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
        eventList = ["ping", "update:project", "create:job", "update:job", "delete:task", "create:issue", "create:comment", "delete:issue", "update:issue"]
        if data["event"] == eventList[0]: # 测试 webhook 是否畅通
            username = data['sender']["username"]
            logger.info(f"@{username} ping webhook successful !")
            
        if data["event"] == eventList[1]: # 更新项目名字/标签
            pass
        if data["event"] == eventList[2]: # 创建标注任务
            createTaskTime = data["task"]["created_date"]
            taskName = data["task"]["name"] # 任务名字
            taskId = data["task"]["id"] # 任务ID
            taskProId = data["task"]["project_id"] # 项目ID
            create_task_owner = data["task"]["owner"]["username"] # 创建人
            taskdimension = data["task"]["dimension"] # 任务类型：2D 、3D
            webhookSend = data["sender"]["username"] # webhook 触发者
            # 这里需要获取 该任务的 总帧数 和 所在的项目名字是哪个
            task_keyframe_count = get_task_info(taskId)
            task_in_project_name = get_project_info(taskProId)
            
        if data["event"] == eventList[3]: # 更新标注任务状态
            pass
        if data["event"] == eventList[4]: # 删除标注任务
            pass
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
        wb_dingtalk("error", "")
        return app.response_class(status=404)




app.run(host=config.APP_HOST,port=config.APP_PORT, debug=config.APP_DEBUG)

'''
create:task
    '{
        "event": "create:task", 
        "task": {
            "url": "http://10.4.10.254:8080/api/tasks/2013", 
            "id": 2013, 
            "name": "testg", 
            "project_id": 73, 
            "mode": "", 
            "owner": {
                "url": "http://10.4.10.254:8080/api/users/1", 
                "id": 1, 
                "username": "guoweitao", 
                "first_name": "guo", "
                last_name": "weitao"
            }, 
            "assignee": null, 
            "bug_tracker": "", 
            "created_date": "2023-04-14T07:05:47.803730Z", 
            "updated_date": "2023-04-14T07:05:47.830569Z", 
            "overlap": null, 
            "segment_size": 0, 
            "status": "annotation", 
            "dimension": "2d", 
            "subset": "", 
            "organization": null, 
            "target_storage": {
                "id": 100,
                "location": "local", 
                "cloud_storage_id": null
            }, 
            "source_storage": {
                "id": 99, 
                "location": "local", 
                "cloud_storage_id": null
            }, 
            "jobs": {
                "count": 0, 
                "completed": 0, 
                "url": "http://10.4.10.254:8080/api/jobs?task_id=2013"
            }, 
            "labels": {
                "count": 4, 
                "url": "http://10.4.10.254:8080/api/labels?task_id=2013"
            }
        }, 
        "webhook_id": 3, 
        "sender": {
            "url": "http://10.4.10.254:8080/api/users/1", 
            "id": 1, 
            "username": "guoweitao", 
            "first_name": "guo", 
            "last_name": "weitao"
        }
    }'

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

delete:task
    '{
        "event": "delete:task",
        "task": {
            "url": "http://10.4.10.254:8080/api/tasks/2010",
            "id": 2010, "name": "test", "project_id": 73, "mode": "annotation", 
            "owner": {
                "url": "http://10.4.10.254:8080/api/users/1",
                "id": 1, "username": "guoweitao", "first_name": "guo", "last_name": "weitao"
            }, 
            "assignee": null, "bug_tracker": "", "created_date": "2023-04-14T03:37:30.488294Z",
            "updated_date": "2023-04-14T03:51:52.640062Z", "overlap": 0, "segment_size": 1,
            "status": "validation", "data_chunk_size": 32,
            "data_compressed_chunk_type": "imageset", 
            "data_original_chunk_type": "imageset", "size": 1, "image_quality": 70, 
            "data": 1973, "dimension": "2d", "subset": "", "organization": null, 
            "target_storage": {
                "id": 92, "location": "local", "cloud_storage_id": null
            }, 
            "source_storage": {
                "id": 91, "location": "local", "cloud_storage_id": null
            },
            "jobs": {
                "count": 1, "completed": 0, "url": "http://10.4.10.254:8080/api/jobs?task_id=2010"
            }, 
            "labels": {
                "count": 4, "url": "http://10.4.10.254:8080/api/labels?task_id=2010"
            }
        },
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