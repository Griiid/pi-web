from .exchange_rate import exchange_rate
from .uniqlo_price import uniqlo_price

_FUNCTION_MAPPING = {}
_FUNCTION_MAPPING_TEMP = {
    exchange_rate: ["匯率"],
    uniqlo_price: ["UQ"],
}

for func, keys in _FUNCTION_MAPPING_TEMP.items():
    for key in keys:
        _FUNCTION_MAPPING[key] = func


def process_text(message, reply_token):
    text = message["text"]
    text_split = text.split(" ")
    func = _FUNCTION_MAPPING.get(text_split[0])
    if func:
        func(text_split[1:], reply_token)
