import json
import traceback


def print_traceback():
    print("\x1B[1;31m" f"{traceback.format_exc()}" "\x1B[m")


def print_error(text):
    print("\x1B[1;31m" f"{text}" "\x1B[m")


def print_item(item_name, text):
    print("\x1B[1;32;7m" f" {item_name} " "\x1B[m " f"{text}")


def print_json(json_obj, item_name=None):
    text = json.dumps(json_obj, indent=2)
    if item_name:
        print_item(item_name, text)
    else:
        print(text)
