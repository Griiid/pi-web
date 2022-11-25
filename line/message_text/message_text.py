from .exchange_rate import exchange_rate
from utils.print import (
    print_error,
    print_item,
    print_json,
)

FUNCTION_MAPPING = {
    "匯率": exchange_rate,
}


def process_text(message, reply_token):
    text = message["text"]
    text_split = text.split(" ")
    func = FUNCTION_MAPPING.get(text_split[0])
    if func:
        func(text_split[1:], reply_token)