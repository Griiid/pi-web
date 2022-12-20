import sqlite3

from flask import (
    Flask,
    request,
)
from flask_socketio import (
    SocketIO,
    emit,
)
from flask import (
    Blueprint,
    Response,
    abort,
    jsonify,
    render_template,
    request,
    send_from_directory,
)

from app import socketio

kk = Blueprint("kk", __name__, url_prefix="/kk", template_folder="templates", static_folder="static")


@kk.route("/status", methods=['GET'])
def upload():
    if not request.json:
        abort(400)

    d = request.json.get("data", 0)
    print("receive data:{}".format(d))
    # do something

    # 回傳給前端
    socketio.emit('status_response', {'data': d})
    return jsonify(
        {"response": "ok"}
    )


@socketio.on('start')
def handle_start():
    con = sqlite3.connect('../mud/kk.sqlite')
    cur = con.cursor()
    cur.execute(
        "SELECT datetime(timestamp, 'localtime') as t, msg " \
        "FROM tb_msg " \
        "WHERE t >= DATE('now', '-3 days')"
    )
    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append({
            'datetime': row[0],
            'msg': row[1],
        })
    return data


@kk.route("/emit_kingdom_msg", methods=['POST'])
def emit_kingdom_msg():
    if not request.json:
        abort(400)
    data = request.json
    msg_id = data.get('id', None)
    if not msg_id:
        abort(400)
    con = sqlite3.connect('kk.sqlite')
    cur = con.cursor()
    cur.execute(f"SELECT datetime(timestamp, 'localtime') as timestamp, msg FROM tb_msg WHERE id={msg_id}")
    row = cur.fetchall()
    if not row:
        abort(400)
    dt = row[0][0]
    msg = row[0][1]
    socketio.emit('msg', {'datetime': dt, 'msg': msg})
    return 'ok'


@kk.route("/")
def home():
    return render_template('index.html', async_mode=socketio.async_mode)


@kk.route("/test.html")
def test():
    return render_template('test.html')


@kk.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@kk.route('/styles/<path:path>')
def send_style(path):
    return send_from_directory('static/styles', path)
