from flask import Flask, Response, request

from .rss import make_feed


app = Flask(__name__)


@app.route('/@<userid>')
def index(userid):
    print(userid)
    response = Response(
        make_feed(userid),
        mimetype='text/xml')

    return response.make_conditional(request)
