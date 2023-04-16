# cvat-webhook-event 消息通知字段整理
<div align="center">
    <img src="../webhooks-banner.svg">
</div>

## <font color="red">注意：每次通知都带上当前北京时间点</font>

### 更新项目名字
```Python
# update:project
    project_id = info["project"]["id"] # 项目ID

    project_name = info["project"]["name"] # 项目名字

    project_touch_owner = info["project"]["owner"]["username"] # 该项目是 谁创建的

    project_rename_owner = info["sender"]["username"] # 谁改的该项目名字

    try:
        project_before_name = info["before_update"]["name"] # 之前的项目名字
    except:
        # warning
    
    # 这里可根据 project_id 生成 内网、外网 项目访问地址
```

### 删除项目
```Python
# delete:project
    project_id = info["project"]["id"] # 项目ID

    project_name = info["project"]["name"] # 项目名字

    project_touch_owner = info["project"]["owner"]["username"] # 该项目是 谁创建的

    project_del_owner = info["sender"]["username"] # 谁删除的该项目
```

### 创建任务
```Python
# create:job
    task_job_id = info["job"]["id"] # job id

    task_id = info["job"]["task_id"] # 任务id

    task_project_id = info["job"]["project_id"] # 任务所在项目id

    task_dimension = info["job"]["dimension"] # 任务类型 2D、3D

    task_status = info["job"]["status"] # 任务状态 标注、验收、完成

    task_stage = info["job"]["stage"] # (标注 | 验收 | 完成)

    task_stage_state = info["job"]["state"] # (标注 | 验收 | 完成)状态 (开始 | 进行中 | 拒绝 | 完成)

    task_start_frame_count = info["job"]["stop_frame"] + 1 # 该任务的总帧数
    
    task_create_user = info["sender"]["username"] # 该任务由谁创建

    # 这里根据 task_id 获取 该任务名字
    # 这里根据 project_id 获取 该任务所在项目的项目名字
    # 这里根据 config 配置文件 及 job_id 和 task_id 生成 该任务的 内网&外网 的访问地址
```

### 删除任务
```Python
# delete:task
    task_del_id = info["task"]["id"] # 被删除的任务ID
    
    task_del_name = info["task"]["name"] # 被删除的任务名字
    
    task_del_project_id = info["task"]["project_id"] # 在哪个项目中删除的该任务

    task_del_dimension = info["task"]["dimension"] # 被删除的任务类型

    task_touch_owner = info["task"]["owner"]["username"] # 谁创建的该任务

    task_del_owner = info["task"]["sender"]["username"] # 谁删除的该任务

    # 这里根据 project_id 获取 该任务所在项目的名字
```

### 任务状态
```Python
# update:job
    task_id = info["job"]["task_id"]

    task_job_id = info["job"]["id"]

    task_project_id = info["job"]["project_id"]

    task_dimension = info["job"]["dimension"]

    task_status = info["job"]["status"]

    task_stage = info["job"]["stage"]

    task_state = info["job"]["state"]
    
    task_upd_owner = info["sender"]["username"]

    # 这里要根据 status stage state 三个状态来判断用户是否按正常流程操作，并正确提示当前任务状态
```

### 创建批注
```Python
# create:comment
    comment_issue_id = info["comment"]["id"] # 批注ID

    comment_message = info["comment"]["message"] # 批语

    comment_create_owner = info["comment"]["owner"]["username"] # 谁创建的批注


    # 这里根据 comment_issue_id 获取 job_id 和 frame
    # 这里根据 job_id 获取对应的 task_id 然后，用 task_id 和 job_id 和 frame 生成内网、外网访问地址
```

### 批注状态
```Python
# update:issue
    issue_id = info["issue"]["id"]

    issue_frame = info["issue"]["frame"] # 第几帧上的批注

    issue_job_id = info["issue"]["job"] # 批注所在的job

    issue_create_owner = info["issue"]["owner"]["username"] # 批注是谁所创建的

    issue_resolved = info["issue"]["resolved"] # 批注状态：true false 是否已解决

    issue_upd_owner = info["sender"]["username"] # 谁改变的批注状态
```

### 删除批注
```Python
# delete:issue
    issue_id = info["issue"]["id"] # 批注的ID

    issue_frame = info["issue"]["frame"] # 第几帧上的批注

    issue_job_id = info["issue"]["job"] # 批注所在的job

    issue_create_owner = info["issue"]["owner"]["username"] # 批注是谁所创建的

    issue_del_owner = info["sender"]["username"] # 批注是谁删除的
```