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

from collections import defaultdict

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
    return getSearchResults(getSearchText(req))

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


def search_results_from_keyphrases(l):
    """
    Input:

    l: list of keyphrases

    Output:

    output: dictionary of results where
        key: the input keyphrase
        value: list of ranked output with each item in tuple of
               (score, name of element)

    """

    output = defaultdict(list)

    for kw in l:
        # calling search function on each keyword
        # TODO this may change to elasticsearch client directly
        search_result = getSearchResults(kw)

        # check if there's no result returned
        if search_result != {}:
            output[kw]  = [ (o['score'], o['name'] ) for o in search_result['results']]

    return output

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')


    # test search result from keyphrase
    # kp = ['car', 'toyota', 'whatever']
    #
    # search_results_from_keyphrases(kp)
