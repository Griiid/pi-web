import requests

from .config import ACCESS_TOKEN


URL_MESSAGE_REPLY = "https://api.line.me/v2/bot/message/reply"


def line_message_object_text(text):
    return {
        "type": "text",
        "text": text,
    }



def send_reply_message(event, messages):
    print(messages)
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
    }
    data = {
        "replyToken": event["replyToken"],
        "messages": messages,
    }

    r = requests.post(URL_MESSAGE_REPLY, json=data, headers=headers)
    print(f"{r.status_code} {r.text}")
