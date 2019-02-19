from flask import Flask

app = None

def init():
    app = Flask(__name__)
    app.debug = True

def getApp():
    if app == None:
        init()

    return app

