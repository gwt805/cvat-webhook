from dingtalkchatbot.chatbot import DingtalkChatbot
import urllib.parse, hashlib, base64, time, hmac
from loguru import logger
import threading, random
import config
import requests

def random_color():
    color_code = "0123456789ABCDEF"
    color_str = "".join([random.choice(color_code) for item in range(6)])
    return color_str

def dingtalk(flag, data):
    eventList = config.EVENT_LIST
    if flag == eventList[0]:
        msg_text = f"### <font color={random_color()}>{data}</font>"
    if flag == eventList[1]:
        msg_text = f"### <font color={random_color()}></font>"
    if flag == eventList[2]:
        msg_text = f"<font color={random_color()}>{data['createTaskTime']}</font> 时, <font color={random_color()}>@{data['create_task_owner']}</font> 在 <font color={random_color()}>{data['task_in_project_name']}</font> 项目中创建了一条 <font color={random_color()}>{data['taskdimension']}</font> 标注记录,详情如下:\n\r&emsp; 任务ID: <font color={random_color()}>{data['taskId']}</font>\n\r&emsp; 任务名字: <font color={random_color()}>{data['taskName']}</font>\n\r&emsp;<font color={random_color()}>[内网访问]({config.BASE_URL.replace('api','task/' + data['taskId'])})</font>&emsp;<font color={random_color()}>[外网访问]({config.OUTER_NET_ADDRESS + '/task/' + data['taskId']})</font>\n\r注: 本条消息由 <font color={random_color()}>cvat-webhook</font> 触发"
    if flag == eventList[3]:
        msg_text = f"### <font color={random_color()}></font>"
    if flag == eventList[4]:
        msg_text = f"<font color={random_color()}>{data['del_task_time']}</font> 时, <font color={random_color()}>@{data['del_task_owner']}</font> 在 <font color={random_color()}>{data['del_task_ProName']}</font> 项目中删除了一条 <font color={random_color()}>{data['del_task_dimension']}</font> 标注记录,详情如下:\n\r&emsp; 任务ID: <font color={random_color()}>{data['del_task_id']}</font>\n\r&emsp; 任务名字: <font color={random_color()}>{data['del_task_name']}</font>\n\r&emsp; 任务状态: <font color={random_color()}>{data['del_task_status']}</font>\n\r注: 本条消息由 <font color={random_color()}>cvat-webhook</font> 触发"
    if flag == eventList[5]:
        msg_text = f"### <font color={random_color()}></font>"
    if flag == eventList[6]:
        msg_text = f"### <font color={random_color()}></font>"
    if flag == eventList[7]:
        msg_text = f"### <font color={random_color()}></font>"
    if flag == "error":
            msg_text = f"### <font color={random_color()}>cvat webhook 配置错误!</font>"
    
    def ding_mes():
        timestamp = str(round(time.time() * 1000))
        secret = config.DING_ROBOT_SECRET  # 替换成你的签
        secret_enc = secret.encode("utf-8")
        string_to_sign = "{}\n{}".format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode("utf-8")
        hmac_code = hmac.new(
            secret_enc, string_to_sign_enc, digestmod=hashlib.sha256
        ).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        # 引用钉钉群消息通知的Webhook地址：
        webhook = f"https://oapi.dingtalk.com/robot/send?access_token={config.DING_ROBOT_WEBHOOK_TOKEN}&timestamp={timestamp}&sign={sign}"
        # 初始化机器人小丁,方式一：通常初始化
        msgs = DingtalkChatbot(webhook)
        
        states = msgs.send_markdown(title="cvat-robot", text=msg_text, is_at_all=False)
        logger.info(f"钉钉机器人消息状态: {states}")

    def wecom_mes():
        res = requests.post(
            f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={config.WECOM_ROBOT_WEBHOOK_KEY}", 
            json={
                "msgtype": "markdown",
                "markdown": {
                    "content": msg_text.replace("&emsp;", "    ")
                }
            }
        )
        logger.info(f"企微机器人消息状态: {res.json()}")
    
    task_ding = threading.Thread(target=ding_mes)
    task_wecom = threading.Thread(target=wecom_mes)

    if config.DING_ROBOT_WEBHOOK_TOKEN == "" or config.DING_ROBOT_SECRET == "":
        logger.warning('钉钉机器人还没有配置好喔!')
    else:
        task_ding.start()
    if config.WECOM_ROBOT_WEBHOOK_KEY == "":
        logger.warning("企业微信机器人还没有配置喔！")
    else:
        task_wecom.start()
