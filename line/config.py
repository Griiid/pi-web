from flask import current_app

CHANNEL_SECRET = current_app.config["CHANNEL_SECRET"]
ACCESS_TOKEN = current_app.config["ACCESS_TOKEN"]
