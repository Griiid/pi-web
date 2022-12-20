from exceptions import MyBasicException
from flask import (
    Flask,
    Response,
)
from werkzeug.exceptions import HTTPException

from app import create_app
from utils import status
from utils.print import (
    print_error,
    print_traceback,
)

app = create_app()


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    if app.debug:
        print_traceback()
    else:
        print_error(f"Exception: {e}")

    if isinstance(e, MyBasicException):
       return Response("", status=e.status)
    else:
        return Response("", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@app.route("/", methods=["GET"])
def index():
    return "INDEX"
