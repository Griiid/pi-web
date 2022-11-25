import json
import requests

from ..constants import (
    FLEX_END,
    FLEX_SEPARATOR,
    FLEX_START,
)
from ..message_api import send_reply_message
from utils.print import print_json

_FLEX_START = FLEX_START.format(title="Uniqlo 搜尋", title_color="#FFFFFF")
_FLEX_END = FLEX_END.format(header_background="#FD0000")

_FLEX_CONTENT_PRICE = '{{"type":"box","layout":"vertical","contents":[{{"type":"box","layout":"baseline","contents":[{{"type":"text","text":"{product_number}","size":"lg","weight":"bold"}},{{"type":"text","text":"{sex}","align":"end","color":"#AAAAAA"}}]}},{{"type":"text","text":"{name}","wrap":true}},{{"type":"box","layout":"horizontal","contents":[{{"type":"box","layout":"vertical","contents":[{{"type":"box","layout":"baseline","contents":[{{"type":"text","text":"價格","adjustMode":"shrink-to-fit","flex":2,"color":"#aaaaaa"}},{{"type":"text","text":"${origin_price}","flex":5,"color":"#CCCCCC"}}],"spacing":"md"}}],"flex":6}},{{"type":"image","url":"{main_picture}","flex":4,"align":"center"}}]}}],"action":{{"type":"uri","label":"action","uri":"{link}"}}}}'
_FLEX_CONTENT_PRICE_CHEAP = '{{"type":"box","layout":"vertical","contents":[{{"type":"box","layout":"baseline","contents":[{{"type":"text","text":"{product_number}","size":"lg","weight":"bold"}},{{"type":"text","text":"{sex}","align":"end","color":"#AAAAAA"}}]}},{{"type":"text","text":"{name}","wrap":true}},{{"type":"box","layout":"horizontal","contents":[{{"type":"box","layout":"vertical","contents":[{{"type":"box","layout":"baseline","contents":[{{"type":"text","text":"特價","adjustMode":"shrink-to-fit","flex":2,"color":"#aaaaaa"}},{{"type":"text","text":"${new_prices} 🥳","flex":5,"size":"xl","color":"#EAA000"}}],"spacing":"md"}},{{"type":"box","layout":"baseline","contents":[{{"type":"text","text":"原價","adjustMode":"shrink-to-fit","flex":2,"color":"#aaaaaa"}},{{"type":"text","text":"${origin_price}","flex":5,"decoration":"line-through","color":"#CCCCCC"}}],"spacing":"md"}}],"flex":6}},{{"type":"image","url":"{main_picture}","flex":4,"align":"center"}}]}}],"action":{{"type":"uri","label":"action","uri":"{link}"}}}}'

_SEARCH_URL = 'https://d.uniqlo.com/tw/p/hmall-sc-service/search/searchWithDescriptionAndConditions/zh_TW'


def uniqlo_price_kernel(product_number):
    headers = {
        "User-Agent": "Firefox/76.0",
        'Content-Type': 'application/json',
    }
    data = {
        "pageInfo": {
            "page": 1,
            "pageSize": 1
        },
        "description": product_number,
        "insiteDescription": product_number,
        "color": [],
        "size": [],
        "season": [],
        "material": [],
        "identity": [],
        "sex": [],
        "rank": "overall",
        "priceRange": {
            "low": 0,
            "high": 0
        }
    }
    r = requests.post(_SEARCH_URL, headers=headers, json=data)
    if r.status_code != 200:
        return None

    resp_data = r.json()
    resp_data = resp_data['resp'][1][0]
    sex = resp_data['sex']
    name = resp_data['name']
    origin_price = int(resp_data['originPrice'])
    prices = resp_data.get('prices', None)
    prices = [int(p) for p in prices]
    product_code = resp_data['productCode']
    main_picture = resp_data['mainPic']
    main_picture = f'https://www.uniqlo.com/tw{main_picture}'
    link = f'https://www.uniqlo.com/tw/zh_TW/product-detail.html?productCode={product_code}'

    result = {
        "product_number": product_number,
        "name": name,
        "sex": sex,
        "origin_price": origin_price,
        "main_picture": main_picture,
        "link": link,
    }
    if isinstance(prices, list):
        if len(prices) == 1:
            if origin_price != prices[0]:
                result["new_prices"] = prices[0]
        else:
            prices = ', '.join(str(int(price)) for price in prices)
            result["new_prices"] = prices
    elif isinstance(prices, str):
        result["new_prices"] = prices
    elif prices is not None:
        result["new_prices"] = f"{prices} ({type(prices)})"

    return result


def uniqlo_price(product_number_list, reply_token):
    """UQ 商品編號 1 [商品編號 2] ..."""
    product_number_list = product_number_list[1:]
    if not product_number_list:
        return

    content_list = []
    for product_number in product_number_list:
        data = uniqlo_price_kernel(product_number)
        if "new_prices" in data:
            content_list.append(_FLEX_CONTENT_PRICE_CHEAP.format(**data))
        else:
            content_list.append(_FLEX_CONTENT_PRICE.format(**data))

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
