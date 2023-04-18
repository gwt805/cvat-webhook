import random
from config import config
from tools.message.send_msg import send_msg

eventList = config.EVENT_LIST

def random_color():
    color_code = "0123456789ABCDEF"
    color_str = "".join([random.choice(color_code) for item in range(6)])
    return color_str

def create_msg(flag, data):
    if flag == eventList[0]:
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['user']}</font> <font color={random_color()}>{data['msg']}</font>"
    if flag == eventList[1]:
        # 谁改了 谁创建的项目名字，详情如下： 原项目名字：xxx 现在项目名字：xxx， 内网访问地址，外网访问地址
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['project_rename_owner']}</font> 改了 <font color={random_color()}>@{data['project_touch_owner']}</font> 创建的项目名字, 详情如下:\n\r&emsp;原项目名: <font color={random_color()}>{data['project_before_name']}</font>\n\r&emsp;现项目名: <font color={random_color()}>{data['project_now_name']}</font>\n\r&emsp;<font color={random_color()}>[内网查看请点我]({data['project_inside_open_addres']})</font>\n\r&emsp;<font color={random_color()}>[外网查看请点我]({data['project_outer_open_addres']})</font>"
    if flag == eventList[2]:
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['project_del_owner']}</font> 删除了 <font color={random_color()}>@{data['project_touch_owner']}</font> 创建的名为<font color={random_color()}>{data['project_name']}</font> 的项目"
    if flag == eventList[3]:
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['task_create_user']}</font> 创建了一个 <font color={random_color()}>{data['task_dimension']}</font> 标注任务, 详情如下:\n\r&emsp;任务ID: <font color={random_color()}>{data['task_id']}</font>\n\r&emsp;任务名字: <font color={random_color()}>{data['task_name']}</font>\n\r&emsp;任务所在项目名字: <font color={random_color()}>{data['task_project_name']}</font>\n\r&emsp;任务总帧数: <font color={random_color()}>{data['task_frame_count']}</font>\n\r&emsp;<font color={random_color()}>[内网查看请点我]({data['project_inside_open_addres']})</font>\n\r&emsp;<font color={random_color()}>[外网查看请点我]({data['project_outer_open_addres']})</font>"
    if flag == eventList[4]:
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['task_del_owner']}</font> 删除了 <font color={random_color()}>@{data['task_touch_owner']}</font> 创建的标注任务, 详情如下:\n\r&emsp;任务ID: <font color={random_color()}>{data['task_del_id']}</font>\n\r&emsp;任务名字: <font color={random_color()}>{data['task_del_name']}</font>\n\r&emsp;任务类型: <font color={random_color()}>{data['task_del_dimension']}</font>"
    if flag == eventList[5]:
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['task_upd_owner']}</font> 在项目 <font color={random_color()}>{data['task_project_name']}</font> 中更新了一条标注记录的任务的状态, 详情如下:\n\r&emsp;任务ID: <font color={random_color()}>{data['task_id']}</font>\n\r&emsp;任务名字: <font color={random_color()}>{data['task_name']}</font>\n\r&emsp;任务类型: <font color={random_color()}>{data['task_dimension']}</font>\n\r&emsp;任务所在阶段: <font color={random_color()}>{data['task_stage']}</font>\n\r&emsp;该阶段状态: <font color={random_color()}>{data['task_state']}</font>\n\r&emsp;<font color={random_color()}>[内网查看请点我]({data['project_inside_open_addres']})</font>\n\r&emsp;<font color={random_color()}>[外网查看请点我]({data['project_outer_open_addres']})</font>"
    if flag == eventList[6]:
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['comment_create_owner']}</font> 在任务<font color={random_color()}>{data['task_name']}</font> 中创建了一条批注记录, 详情如下:\n\r&emsp;批注ID: <font color={random_color()}>{data['comment_issue_id']}</font>\n\r&emsp;批注所在帧数: <font color={random_color()}>{data['frame']}</font>\n\r&emsp;任务ID: <font color={random_color()}>{data['task_id']}</font>\n\r&emsp;批语: <font color={random_color()}>{data['comment_message']}</font>\n\r&emsp;<font color={random_color()}>[内网查看请点我]({data['project_inside_open_addres']})</font>\n\r&emsp;<font color={random_color()}>[外网查看请点我]({data['project_outer_open_addres']})</font>"
    if flag == eventList[7]:
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['issue_del_owner']}</font> 删除了一个由 <font color={random_color()}>@{data['issue_create_owner']}</font> 创建的批注, 详情如下:\n\r&emsp;批注ID: <font color={random_color()}>{data['issue_id']}</font>\n\r&emsp;批注所在帧: <font color={random_color()}>{data['issue_frame']}</font>\n\r&emsp;任务ID: <font color={random_color()}>{data['issue_task_id']}</font>\n\r&emsp;任务名字: <font color={random_color()}>{data['issue_task_name']}</font>"
    if flag == eventList[8]:
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['issue_upd_owner']}</font>更新了一条由 <font color={random_color()}>{data['issue_create_owner']}</font> 创建的批注的状态, 详情如下:\n\r&emsp;批注ID: <font color={random_color()}>{data['issue_id']}</font>\n\r&emsp;批注所在帧: <font color={random_color()}>{data['issue_frame']}</font>\n\r&emsp;批注状态: <font color={random_color()}>{data['issue_resolved']}</font>\n\r&emsp;任务ID: <font color={random_color()}>{data['issue_task_id']}</font>\n\r&emsp;任务名字: <font color={random_color()}>{data['issue_task_name']}</font>\n\r&emsp;<font color={random_color()}>[内网查看请点我]({data['project_inside_open_addres']})</font>\n\r&emsp;<font color={random_color()}>[外网查看请点我]({data['project_outer_open_addres']})</font>"
    if flag == "error":
        msg = f"### <font color={random_color()}>{data['datetime']}</font>\n\r<font color={random_color()}>@{data['msg']}</font>"
    send_msg(msg)