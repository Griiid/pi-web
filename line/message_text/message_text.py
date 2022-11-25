from ..message_api import (
    line_message_object_text,
    send_reply_message,
)
from .exchange_rate import exchange_rate
from .uniqlo_price import uniqlo_price
from .direct_reply import direct_reply


def command_explain(params, reply_token):
    for func in _FUNCTION_MAPPING_TEMP.keys():
        if func is command_explain:
            continue
        print(func.__doc__)

    message = "支援的指令如下，[ ] 裡面的是選擇性輸入\n----\n"
    message += "\n".join([
        func.__doc__
        for func in _FUNCTION_MAPPING_TEMP.keys() if func is not command_explain and func.__doc__ is not None
    ])
    message = line_message_object_text(message)

    send_reply_message(reply_token, [message])


_FUNCTION_MAPPING = {}
_FUNCTION_MAPPING_TEMP = {
    command_explain: ["help", "?"],
    exchange_rate: ["匯率"],
    uniqlo_price: ["UQ"],
    direct_reply: ["豪豪", "容容"],
}

for func, keys in _FUNCTION_MAPPING_TEMP.items():
    for key in keys:
        _FUNCTION_MAPPING[key] = func


def process_text(message, reply_token):
    text = message["text"]
    text_split = text.split(" ")
    func = _FUNCTION_MAPPING.get(text_split[0])
    if func:
        func(text_split, reply_token)
