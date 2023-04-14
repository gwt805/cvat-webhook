from dingtalkchatbot.chatbot import DingtalkChatbot
from loguru import logger
import urllib.parse
import threading
import hashlib
import config
import base64
import time
import hmac

def wb_dingtalk(flag, msg):
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
        
        if flag == "error":
            msg_text = "webhook 配置错误!"
        
        states = msgs.send_text(msg=(msg_text), is_at_all=False)
        logger.info(f"消息状态: {states}")
    
    task = threading.Thread(target=ding_mes)
    if config.DING_ROBOT_WEBHOOK_TOKEN == "" or config.DING_ROBOT_SECRET == "":
        logger.warning('钉钉机器人还没有配置好喔!')
    else:
        task.start()