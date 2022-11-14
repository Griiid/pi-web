from exceptions import MyBasicException
from flask import (
    Flask,
    Response,
)
from werkzeug.exceptions import HTTPException

from utils import status
from utils.print import (
    print_error,
    print_traceback,
)

app = Flask(__name__)
app.config.from_prefixed_env()

with app.app_context():
    from line.line import line
    app.register_blueprint(line)


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
