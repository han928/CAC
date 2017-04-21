#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os
import urllib2

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/audiencecreation', methods=['POST'])
def audiencecreation():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    print("Response:")
    print(res)

    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
    text = getSearchText(req)

    # DO SOME DATA SCIENCE FUN STUFF

    
    return getSearchResults(text)

def getSearchText(req):
    if req and req['message'] and req['message'] is not None:
        return req['message']
    else:
        return

def getSearchResults(text):

    print("Search Text:")
    print(text)

    if text:
        req = urllib2.Request("http://13.91.7.37/api/v1/search?" + urlencode({'term': text}) + "&offset=0&rows=100")
        req.add_header('Authorization', 'Bearer 8799eb0c-a8b4-4362-8706-30955b57df74')
        result = urllib2.urlopen(req).read()
        return json.loads(result)
    else:
        return {}

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
