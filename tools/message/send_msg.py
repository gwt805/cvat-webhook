from dingtalkchatbot.chatbot import DingtalkChatbot
import urllib.parse, hashlib, base64, time, hmac
from loguru import logger
import threading
from config import config
import requests

def send_msg(msg_text):
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
        logger.warning("钉钉机器人还没有配置好喔!")
    else:
        task_ding.start()
    if config.WECOM_ROBOT_WEBHOOK_KEY == "":
        logger.warning("企业微信机器人还没有配置喔!")
    else:
        task_wecom.start()
