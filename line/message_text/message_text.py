from utils.print import (
    print_error,
    print_item,
    print_json,
)

from .exchange_rate import exchange_rate


FUNCTION_MAPPING = {
    "匯率": exchange_rate,
}


def process_text(message, reply_token):
    text = message["text"]
    func = FUNCTION_MAPPING.get(text)
    if func:
        func(text, reply_token)
