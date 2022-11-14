import requests

URL_EXCHANGE_RATE = "https://rate.bot.com.tw/xrt/flcsv/0/day"


def exchange_rate(text, reply_token):
    r = requests.get(URL_EXCHANGE_RATE)
