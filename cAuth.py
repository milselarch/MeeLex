import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import http.server

import argparse as argparser
import datetime
import logging
import socket
import sys

from six.moves import http_client
from six.moves import input
from six.moves import urllib

from oauth2client import _helpers
from oauth2client import client

import config
import json

"""
tools.run_flow library code
"""

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'data/client_secret_web.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

"""
tools.run_flow library code
"""

def makeAuthLink(flow=None, redirect=False, host=None, port=None):

    if flow == None:
        flow = client.flow_from_clientsecrets(
            CLIENT_SECRET_FILE, SCOPES
        )
        flow.user_agent = APPLICATION_NAME

    if redirect == True:
        if port == None:
            oauth_callback = 'http://{host}'.format(host=host)
        else:
            oauth_callback = 'http://{host}:{port}'.format(
                host=host, port=port
            )

    else:
        oauth_callback = client.OOB_CALLBACK_URN

    flow.redirect_uri = oauth_callback
    flow.state = "123123123"
    authorize_url = flow.step1_get_authorize_url()
    return authorize_url, flow


def JsonToFlow(flowJson):
    flow = client.OAuth2WebServerFlow(**flowJson)
    return flow

def flowToJson(flow):
    return json.dumps({
        "redirect_uri": flow.redirect_uri,
        "auth_uri": flow.auth_uri,
        "token_uri": flow.token_uri,
        "login_hint": flow.login_hint,
        "client_id": flow.client_id,
        "client_secrets": flow.client_secret
    })


def authHandleCode(flow, code):
    credential = flow.step2_exchange(code, http=None)
    return credential

def authHandleRequest(flow, httpd):
    if httpd == None: return
    httpd.handle_request()

    if 'error' in httpd.query_params:
        sys.exit('Authentication request was rejected.')
    if 'code' in httpd.query_params:
        code = httpd.query_params['code']
    else:
        raise ValueError("code query parameter not found")

    try:
        credential = flow.step2_exchange(code, http=None)
        print("CREDS", credential)
        print(help(credential))

    except client.FlowExchangeError as e:
        print(e)
        raise client.FlowExchangeError

    #storage.put(credential)
    #credential.set_store(storage)
    print('Authentication successful.')
    return credential

def makeCredential(json):
    credential = client.OAuth2Credentials.from_json(json)
    return credential