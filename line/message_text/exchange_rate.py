import json
from io import StringIO

import pandas as pd
import requests

from ..constants import (
    FLEX_END,
    FLEX_SEPARATOR,
    FLEX_START,
)
from ..message_api import send_reply_message
from utils.print import print_json

URL_EXCHANGE_RATE = "https://rate.bot.com.tw/xrt/flcsv/0/day"

currency_map = {
    "美金": "USD",
    "美元": "USD",
    "美圓": "USD",
    "美國": "USD",
    "港幣": "HKD",
    "香港": "HKD",
    "英鎊": "GBP",
    "英國": "GBP",
    "澳幣": "AUD",
    "澳洲": "AUD",
    "加拿大幣": "CAD",
    "加拿大": "CAD",
    "新加坡幣": "SGD",
    "新加坡": "SGD",
    "瑞士法郎": "CHF",
    "瑞士": "CHF",
    "日圓": "JPY",
    "日幣": "JPY",
    "日本": "JPY",
    "南非幣": "ZAR",
    "南非": "ZAR",
    "瑞典幣": "SEK",
    "瑞典": "SEK",
    "紐元": "NZD",
    "紐圓": "NZD",
    "紐西蘭": "NZD",
    "泰幣": "THB",
    "泰國": "THB",
    "菲國比索": "PHP",
    "菲律賓": "PHP",
    "印尼幣": "IDR",
    "印尼": "IDR",
    "歐元": "EUR",
    "歐圓": "EUR",
    "歐盟": "EUR",
    "韓元": "KRW",
    "韓圓": "KRW",
    "韓國": "KRW",
    "越南盾": "VND",
    "越南": "VND",
    "馬來幣": "MYR",
    "馬來西亞": "MYR",
    "人民幣": "CNY",
    "中國": "CNY",
}

currency_display_map = {
    "USD": "🇺🇸 美元",
    "HKD": "🇭🇰 港幣",
    "GBP": "🇬🇧 英鎊",
    "AUD": "🇦🇺 澳幣",
    "CAD": "🇨🇦 加拿大幣",
    "SGD": "🇸🇬 新加坡幣",
    "CHF": "🇨🇭 瑞士法郎",
    "JPY": "🇯🇵 日幣",
    "ZAR": "🇿🇦 南非幣",
    "SEK": "🇸🇪 瑞典幣",
    "NZD": "🇳🇿 紐圓",
    "THB": "🇹🇭 泰幣",
    "PHP": "🇵🇭 菲國比索",
    "IDR": "🇮🇩 印尼幣",
    "EUR": "🇪🇺 歐元",
    "KRW": "🇰🇷 韓圓",
    "VND": "🇻🇳 越南盾",
    "MYR": "🇲🇾 馬來幣",
    "CNY": "🇨🇳 人民幣",
}


_FLEX_START = FLEX_START.format(title="匯率查詢結果")
_FLEX_END = FLEX_END.format(header_background="#FFFED1")

FLEX_CONTENT_CURRENCY = '{{"type":"box","layout":"vertical","contents":[{{"type":"text","text":"{currency}","size":"lg","weight":"bold","align":"center","margin":"5px"}},{{"type":"box","layout":"horizontal","paddingStart":"30px","contents":[{{"type":"text","text":" ","flex":2,"size":"lg","weight":"bold","decoration":"none","contents":[]}},{{"type":"text","text":"現金","flex":6}},{{"type":"text","text":"即期","flex":6}}]}},{{"type":"box","layout":"horizontal","paddingStart":"30px","contents":[{{"type":"text","text":"買","flex":2,"color":"#EB4726"}},{{"type":"text","text":"{cash_buy}","flex":6,"color":"#EB4726"}},{{"type":"text","text":"{spot_buy}","flex":6,"color":"#EB4726"}}]}},{{"type":"box","layout":"horizontal","paddingStart":"30px","contents":[{{"type":"text","text":"賣","flex":2,"color":"#43952A"}},{{"type":"text","text":"{cash_sell}","flex":6,"color":"#43952A"}},{{"type":"text","text":"{spot_sell}","flex":6,"color":"#43952A"}}]}}]}}'


def exchange_rate(currency_list, reply_token):
    """匯率 [幣別 1] [幣別 2] ..."""
    r = requests.get(URL_EXCHANGE_RATE)
    if r.status_code != 200:
        print(f'Request failed, status code: {r.status_code}')
        return

    content = r.content.decode("utf-8")
    content_string_io = StringIO(content)
    df = pd.read_csv(content_string_io, sep=",", index_col=False)
    data = df.to_dict("records")

    currency_data_dict = {}
    for data_ in data:
        currency = data_["幣別"]
        currency_display = currency_display_map[currency]
        currency_data_dict[currency] = {
            "currency": currency_display,
            "cash_buy": data_["現金"],
            "spot_buy": data_["即期"],
            "cash_sell": data_["現金.1"],
            "spot_sell": data_["即期.1"],
        }

    if currency_list:
        currency_list = list(filter(lambda c: c is not None, map(lambda c: currency_map.get(c, None), currency_list)))
    else:
        currency_list = currency_data_dict.keys()

    content_list = []
    for currency in currency_list:
        currency_data = currency_data_dict.get(currency, None)
        if currency_data is None:
            continue

        content_list.append(FLEX_CONTENT_CURRENCY.format(**currency_data))

    if not content_list:
        # TODO: 回傳查無資料
        return

    message = "".join([
        _FLEX_START,
        f",{FLEX_SEPARATOR},".join(content_list),
        _FLEX_END,
    ])
    message = json.loads(message)

    print_json(message, "message")
    send_reply_message(reply_token, messages=[message])


if __name__ == '__main__':
    exchange_rate(["美金", "日幣"], None)
