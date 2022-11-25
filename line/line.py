import base64
import hashlib
import hmac
import json
import threading

from flask import (
    Blueprint,
    Response,
    request,
)

from .config import (
    ACCESS_TOKEN,
    CHANNEL_SECRET,
)
from .message_text.message_text import process_text
from exceptions import ForbiddenError
from utils import status
from utils.print import print_json

line = Blueprint("line", __name__, url_prefix="/line")


class MessageHandler:
    FUNCTION_MAPPING = {
        "text": process_text,
    }

    def __init__(self, event):
        self.message = event["message"]
        self.reply_token = event["replyToken"]

    def process(self):
        message_type = self.message["type"]
        func = self.FUNCTION_MAPPING.get(message_type)
        if func:
            func(self.message, self.reply_token)


class EventsHandlerThread(threading.Thread):
    EVENT_HANDLER_MAP = {
        "message": MessageHandler,
    }

    def __init__(self, events):
        threading.Thread.__init__(self)
        self.events = events

    def run(self):
        for event in self.events:
            self._process_event(event)

    @classmethod
    def _process_event(cls, event):
        if event["mode"] != "active":
            return

        event_type = event["type"]
        event_handler = cls.EVENT_HANDLER_MAP.get(event_type)
        if not event_handler:
            return

        event_handler(event).process()


def _verify_signature(body):
    # https://developers.line.biz/en/reference/messaging-api/#signature-validation

    signature = request.headers["x-line-signature"]
    hash = hmac.new(CHANNEL_SECRET.encode("utf-8"), body.encode("utf-8"), hashlib.sha256).digest()
    correct_signature = base64.b64encode(hash).decode("utf-8")
    if signature != correct_signature:
        raise ForbiddenError("Verify signature failed")


@line.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_data(as_text=True)

    _verify_signature(body)

    json_data = json.loads(body)
    print_json(json_data, item_name="body")

    events = json_data.get("events")
    if events:
        EventsHandlerThread(events).start()

    return Response("OK", status=status.HTTP_200_OK)
