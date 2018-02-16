import os

from flask import Flask, Response, request
from raven.contrib.flask import Sentry

from .rss import make_feed

SENTRY_DSN = os.getenv('SENTRY_DSN')

app = Flask(__name__)
if SENTRY_DSN:
    sentry = Sentry(app, dsn=SENTRY_DSN)


@app.route('/@<userid>')
def index(userid):
    print(userid)
    response = Response(
        make_feed(userid),
        mimetype='text/xml')

    return response.make_conditional(request)
