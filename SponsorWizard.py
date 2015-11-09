#!/usr/bin/env python
"""Self-Serve Sponsor Portal for DC2"""

from flask import Flask, request, Response, render_template
import json
import sys
import traceback
import urllib, urllib2
import logging
from logging import FileHandler
# from flask.ext.dotenv import DotEnv
# from config import Config
from environment import *

app = Flask(__name__, static_url_path='/static')
app.config.from_object(__name__)
# env = Config()
# env.init_app(app,env_file=".env")
# print env
# app.config.from_object(Config["DC2Sponsor_config"])

HANDLER = FileHandler(LOGFILE)
HANDLER.setLevel(logging.INFO)
app.logger.addHandler(HANDLER)

ERROR_MESSAGES = {404: "The requested resource cannot be found. What did you do!",
                  401: "You are not authenticated to use this resource. Whatcha doin here?",
                  500: "An error has occurred, but we'll take your money by email :) support@datacommunitydc.org",
                  400: "The request is missing required parameters or otherwise malformed. What are you looking for?"
                  }

ROOT = "/sponsorship"

def make_response(data, code, headers=None):
    """Create a complete JSON response from an object using the Flask Response type"""
    response = Response(json.dumps(data, indent=4)+"\n", status=code, mimetype='application/json')
    response.headers["Server"] = "DC2 Data Lake API"
    if headers != None:
        for key, value in headers.items():
            response.headers[key] = value
    return response

@app.errorhandler(401)
@app.errorhandler(404)
@app.errorhandler(400)
def handle_user_error(err):
    """Handle all 400 level errors. Don't send a support email since this is the user's problem."""
    message = {"status" : "fail",
        "data" : {"reason" : ERROR_MESSAGES[err.code]}}
    app.logger.warning("A user error occurred. code: %i, path: %s", err.code, request.path)
    return make_response(message, err.code)

@app.errorhandler(500)
def handle_internal_error(err):
    """Handle all 500 level errors. Send a detailed email about the error. Respond with a helpful message."""
    message = {"status" : "fail",
        "data" : {"reason" : ERROR_MESSAGES[500]}}
    exc_type, exc_value, exc_traceback = sys.exc_info()
    exc = traceback.format_exception(exc_type,
                                     exc_value,
                                     exc_traceback)
    exc = ''.join(exc)
    error_message = {
           "to": SUPPORTEMAIL,
           "from": "info@datacommunitydc.org",
           "subject": "Sponsor Wizard Error",
           "text": "An error ocurred in the Sponsor Wizard: \n\nENDPOINT: " \
                + request.path + " " + request.method + "\n\n" + exc}
    data = urllib.urlencode(error_message)
    urllib2.urlopen(url="https://api.sendgrid.com/api/mail.send.json", data=data).read()
    app.logger.error("ERROR: " + error_message["text"])
    return make_response(message, 500)

@app.route(ROOT)
def Choose_Sponsor():

    Programs = [{"title":"Data Viz DC","initialism":"DVDC","img":"http://photos4.meetupstatic.com/photos/event/b/2/e/0/global_330165792.jpeg","url":"http://www.meetup.com/Data-Visualization-DC"},
                {"title":"DC2 Digital Nomads","initialism":"DC2DN","img":"http://photos2.meetupstatic.com/photos/event/2/0/c/8/global_333188392.jpeg","url":"http://www.meetup.com/dcnightowls"},
                {"title":"Data Science DC","initialism":"DSDC","img":"http://photos3.meetupstatic.com/photos/event/5/3/4/a/global_393021322.jpeg","url":"http://www.meetup.com/Data-science-DC"},
                {"title":"Data Education DC","initialism":"DEDC","img":"http://photos4.meetupstatic.com/photos/event/c/5/5/global_434463157.jpeg","url":"http://www.meetup.com/Data-Education-DC"},
                {"title":"Women Data Scientists DC","initialism":"WDSDC","img":"http://photos3.meetupstatic.com/photos/event/5/3/4/a/global_393021322.jpeg","url":"http://www.meetup.com/WomenDataScientistsDC/"},
                {"title":"Data Innovation DC","initialism":"DIDC","img":"http://photos2.meetupstatic.com/photos/event/4/1/7/a/global_416596762.jpeg","url":"http://www.meetup.com/Data-business-DC"},
                {"title":"Statistical Programming DC","initialism":"SPDC","img":"http://photos4.meetupstatic.com/photos/event/9/e/c/5/global_441340645.jpeg","url":"http://www.meetup.com/stats-prog-dc"},
                {"title":"Data Wranglers DC","initialism":"DWDC","img":"http://photos2.meetupstatic.com/photos/event/b/4/2/a/global_418006122.jpeg","url":"http://www.meetup.com/Data-wranglers-dc"}
            ]
    # return render_template("test.html")
    return render_template( "WizardHome.html",Programs=Programs)


if __name__ == '__main__':
    #handler = RotatingFileHandler(LOGFILE, maxBytes=1024*1024, backupCount=10)
    handler = FileHandler(LOGFILE)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=FLASKPORT)