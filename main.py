from tools.get_data_info import get_project_info, get_task_info, get_issue_info, get_job_info
from tools.message.create_msg import create_msg
from flask import Flask, request
from config import config
from loguru import logger
import datetime, json
import hashlib, hmac

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    signature = (
        "sha256="
        + hmac.new("mykey".encode("utf-8"), request.data, digestmod=hashlib.sha256).hexdigest()
    )
    datetime_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if hmac.compare_digest(request.headers["X-Signature-256"], signature):
        # logger.info(request.data)
        info = json.loads(request.data)
        eventList = config.EVENT_LIST
        
        if info["event"] == eventList[0]: # "ping"
            username = info['sender']["username"]
            data = {
                "datetime": datetime_now,
                "user": username,
                "msg": "ping cvat webhook succeed !"
            }
            create_msg(eventList[0], data)
            logger.info(f"@{username} ping cvat webhook successful !")
        if info["event"] == eventList[1]: # "update:project"
            project_id = info["project"]["id"] # 项目ID
            project_now_name = info["project"]["name"] # 项目名字
            project_touch_owner = info["project"]["owner"]["username"] # 该项目是 谁创建的
            project_rename_owner = info["sender"]["username"] # 谁改的该项目名字
            project_before_name = info["before_update"]["name"] # 之前的项目名字

            data = {
                "datetime": datetime_now,
                "project_id": project_id,
                "project_now_name": project_now_name,
                "project_before_name": project_before_name,
                "project_touch_owner": project_touch_owner,
                "project_rename_owner": project_rename_owner,
                "project_inside_open_addres": config.BASE_URL + f'/projects/{project_id}',
                "project_outer_open_addres": config.OUTER_NET_ADDRESS + f'/projects/{project_id}'
            }
            create_msg(eventList[1], data)
        if info["event"] == eventList[2]: # "delete:project"
            project_id = info["project"]["id"] # 项目ID
            project_name = info["project"]["name"] # 项目名字
            project_touch_owner = info["project"]["owner"]["username"] # 该项目是 谁创建的
            project_del_owner = info["sender"]["username"] # 谁删除的该项目

            data = {
                "datetime": datetime_now,
                "project_id": project_id,
                "project_name": project_name,
                "project_touch_owner": project_touch_owner,
                "project_del_owner": project_del_owner
            }
            create_msg(eventList[2], data)
        if info["event"] == eventList[3]: # "create:job"
            task_job_id = info["job"]["id"] # job id
            task_id = info["job"]["task_id"] # 任务id
            task_project_id = info["job"]["project_id"] # 任务所在项目id
            task_dimension = info["job"]["dimension"] # 任务类型 2D、3D
            task_frame_count = info["job"]["stop_frame"] + 1 # 该任务的总帧数
            task_create_user = info["sender"]["username"] # 该任务由谁创建
            task_name = get_task_info(task_id) # 获取 该任务名字
            task_project_name = get_project_info(task_project_id) # 获取该任务所在的项目名字
            data = {
                "datetime": datetime_now,
                "task_id": task_id,
                "task_dimension": task_dimension,
                "task_frame_count": task_frame_count,
                "task_create_user": task_create_user,
                "task_name": task_name,
                "task_project_name": task_project_name,
                "project_inside_open_addres": config.BASE_URL + f'/tasks/{task_id}/jobs/{task_job_id}',
                "project_outer_open_addres": config.OUTER_NET_ADDRESS + f'/tasks/{task_id}/jobs/{task_job_id}'
            }
            create_msg(eventList[3], data)
        if info["event"] == eventList[4]: # "delete:task"
            task_del_id = info["task"]["id"] # 被删除的任务ID
            task_del_name = info["task"]["name"] # 被删除的任务名字
            task_del_project_id = info["task"]["project_id"] # 在哪个项目中删除的该任务
            task_del_dimension = info["task"]["dimension"] # 被删除的任务类型
            task_touch_owner = info["task"]["owner"]["username"] # 谁创建的该任务
            task_del_owner = info["sender"]["username"] # 谁删除的该任务
            task_project_name = get_project_info(task_del_project_id) # 这里根据 project_id 获取 该任务所在项目的名字
            
            data = {
                "datetime": datetime_now,
                "task_del_id": task_del_id,
                "task_del_name": task_del_name,
                "task_del_dimension": task_del_dimension,
                "task_touch_owner": task_touch_owner,
                "task_del_owner": task_del_owner
            }
            create_msg(eventList[4], data)
        if info["event"] == eventList[5]: # "update:job"
            stage_to_str = {
                "annotation": "标注",
                "validation": "验收",
                "acceptance": "认可"
            }
            state_to_str = {
                "new": "未开始",
                "in progress": "正在进行中",
                "rejected": "驳回?",
                "completed": "已完成"
            }
            task_id = info["job"]["task_id"]
            task_job_id = info["job"]["id"]
            task_name = get_task_info(task_id)
            task_project_id = info["job"]["project_id"]
            task_project_name = get_project_info(task_project_id)
            task_dimension = info["job"]["dimension"]
            # task_status = info["job"]["status"]
            task_stage = stage_to_str[info["job"]["stage"]]
            task_state = state_to_str[info["job"]["state"]]
            task_upd_owner = info["sender"]["username"]
            
            data = {
                "datetime": datetime_now,
                "task_id": task_id,
                "task_name": task_name,
                "task_project_name": task_project_name,
                "task_dimension": task_dimension,
                "task_stage": task_stage,
                "task_state": task_state,
                "task_upd_owner": task_upd_owner,
                "project_inside_open_addres": config.BASE_URL + f'/tasks/{task_id}',
                "project_outer_open_addres": config.OUTER_NET_ADDRESS + f'/tasks/{task_id}'
            }
            create_msg(eventList[5], data)
        if info["event"] == eventList[6]: # "create:comment"
            comment_issue_id = info["comment"]["issue"] # 批注ID
            comment_message = info["comment"]["message"] # 批语
            comment_create_owner = info["comment"]["owner"]["username"] # 谁创建的批注
            job_id, frame = get_issue_info(comment_issue_id)# 这里根据 comment_issue_id 获取 job_id 和 frame
            task_id = get_job_info(job_id) # 这里根据 job_id 获取对应的 task_id 然后，用 task_id 和 job_id 和 frame 生成内网、外网访问地址
            task_name = get_task_info(task_id)

            data = {
                "datetime": datetime_now,
                "comment_issue_id": comment_issue_id,
                "comment_message": comment_message,
                "comment_create_owner": comment_create_owner,
                "frame": frame,
                "task_id": task_id,
                "task_name": task_name,
                "project_inside_open_addres": config.BASE_URL + f'/tasks/{task_id}/jobs/{job_id}?frame={frame}',
                "project_outer_open_addres": config.OUTER_NET_ADDRESS + f'/tasks/{task_id}/jobs/{job_id}?frame={frame}'
            }
            create_msg(eventList[6], data)
        if info["event"] == eventList[7]: # "delete:issue"
                issue_id = info["issue"]["id"] # 批注的ID
                issue_frame = info["issue"]["frame"] # 第几帧上的批注
                issue_job_id = info["issue"]["job"] # 批注所在的job
                issue_create_owner = info["issue"]["owner"]["username"] # 批注是谁所创建的
                issue_del_owner = info["sender"]["username"] # 批注是谁删除的
                issue_task_id = get_job_info(issue_job_id)
                issue_task_name = get_task_info(issue_task_id)

                data = {
                    "datetime": datetime_now,
                    "issue_id": issue_id,
                    "issue_frame": issue_frame,
                    "issue_create_owner": issue_create_owner,
                    "issue_del_owner": issue_del_owner,
                    "issue_task_name": issue_task_name,
                    "issue_task_id": issue_task_id,
                    "issue_task_name": issue_task_name
                }
                create_msg(eventList[7], data)
        if info["event"] == eventList[8]: # "update:issue"
            resolved_to_str = {'True': '已解决', 'False': '未解决'}
            issue_id = info["issue"]["id"]
            issue_frame = info["issue"]["frame"] # 第几帧上的批注
            issue_job_id = info["issue"]["job"] # 批注所在的job
            issue_create_owner = info["issue"]["owner"]["username"] # 批注是谁所创建的
            issue_resolved = resolved_to_str[str(info["issue"]["resolved"])] # 批注状态：true false 是否已解决
            issue_upd_owner = info["sender"]["username"] # 谁改变的批注状态
            issue_task_id = get_job_info(issue_job_id)
            issue_task_name = get_task_info(issue_task_id)

            data = {
                "datetime": datetime_now,
                "issue_id": issue_id,
                "issue_frame": issue_frame,
                "issue_create_owner": issue_create_owner,
                "issue_resolved": issue_resolved,
                "issue_upd_owner": issue_upd_owner,
                "issue_task_id": issue_task_id,
                "issue_task_name": issue_task_name,
                "project_inside_open_addres": config.BASE_URL + f'/tasks/{issue_task_id}/jobs/{issue_job_id}?frame={issue_frame}',
                "project_outer_open_addres": config.OUTER_NET_ADDRESS + f'/tasks/{issue_task_id}/jobs/{issue_job_id}?frame={issue_frame}'
            }
            create_msg(eventList[8], data)

        return app.response_class(status=200)
    else:
        data = {
                "datetime": datetime_now,
                "msg": "webhook 配置错误!"
            }
        create_msg("error", data)
        logger.error("webhook 配置错误!")
        return app.response_class(status=404)


if __name__=="__main__":
    app.run(host=config.APP_HOST,port=config.APP_PORT, debug=config.APP_DEBUG)