import random

from ..message_api import (
    line_message_object_text,
    send_reply_message,
)

msg_dict = {
    "容容": [
        "好可愛", "超可愛", "有氣質", "好漂亮", "好正", "好美麗", "溫柔", "小聰明", "小花",
        "香比鼻", "森林系", "容貓", "皇后",
    ],
    "豪豪": [
        "好帥", "斯文", "暖男", "可愛", "溫柔", "寵容容", "傻瓜", "臭比鼻",
    ],
}


def direct_reply(key, event):
    if event["source"]["type"] != "group" or event["source"]["groupId"] != "Cb5810e4c4793881749cac3c6c79d0d40":
        return

    key = key[0]
    choices = msg_dict.get(key, None)
    if not choices:
        return

    text = random.choice(msg_dict[key])
    message = line_message_object_text(text)
    send_reply_message(event, [message])
