from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()

def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config.from_prefixed_env()
    app.config['SECRET_KEY'] = '91f9bc0c6be94b438190b721b1b67d15'

    with app.app_context():
        from line.line import line
        from kk.kk import kk
        app.register_blueprint(line)
        app.register_blueprint(kk)

    socketio.init_app(app)

    return app
