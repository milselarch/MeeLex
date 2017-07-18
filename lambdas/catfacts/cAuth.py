import importlib

tools = importlib.__import__("lib.oauth2client.tools")
client = importlib.__import__("lib.oauth2client.client")

import json
import sys

from oauth2client import client

import config

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

def authHandleCode(flow, code):
    credential = flow.step2_exchange(code, http=None)
    return credential

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

def authHandleRequest(code):
    """
    oauth2client.client.FlowExchangeError:
    :param code:
    :return:
    """
    flow = client.flow_from_clientsecrets(
        CLIENT_SECRET_FILE, SCOPES
    )

    flow.user_agent = APPLICATION_NAME
    flow.redirect_uri = "http://boolex.me/auth"
    credential = flow.step2_exchange(code, http=None)
    return credential


def makeCredential(json):
    credential = client.OAuth2Credentials.from_json(json)
    return credential