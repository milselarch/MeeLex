import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import http.server as BaseHTTPServer

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
CLIENT_SECRET_FILE = 'data/client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'

"""
tools.run_flow library code
"""

class ClientRedirectServer(BaseHTTPServer.HTTPServer):
    """
    A server to handle OAuth 2.0 redirects back to localhost.

    Waits for a single request and parses the query parameters
    into query_params and then stops serving.
    """
    query_params = {}

class ClientRedirectHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """A handler for OAuth 2.0 redirects back to localhost.

    Waits for a single request and parses the query parameters
    into the servers query_params and then stops serving.
    """

    def do_GET(self):
        """Handle a GET request.

        Parses the query parameters and prints a message
        if the flow has completed. Note that we can't detect
        if an error occurred.
        """
        self.send_response(http_client.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        parts = urllib.parse.urlparse(self.path)
        query = _helpers.parse_unique_urlencoded(parts.query)
        print("PATH: " + self.path)
        print("QUERY: " + str(query))

        self.server.query_params = query

        self.wfile.write(
            b'<html><head><title>Authentication Status</title></head>')
        self.wfile.write(
            b'<body><p>The authentication flow has completed.</p>')
        self.wfile.write(b'</body></html>')

    def log_message(self, format, *args):
        """
        Do not log messages to stdout while
        running as cmd. line program.
        """

def makeAuthLink(
        hostname, port, flow=None
    ):

    if flow == None:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

    success = False
    port_number = port

    try:
        httpd = ClientRedirectServer(
            (hostname, port),
            ClientRedirectHandler
        )

    except socket.error:
        pass
    else:
        success = True

    if success:
        oauth_callback = 'http://{host}:{port}/'.format(
            host=flags.auth_host_name, port=port_number
        )
    else:
        oauth_callback = client.OOB_CALLBACK_URN

    flow.redirect_uri = oauth_callback
    authorize_url = flow.step1_get_authorize_url()
    return authorize_url, httpd, flow


def authHandleRequest(flow, httpd):
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

def run_flow(
        flow, storage, hostname, port, http=None
    ):

    success = False
    port_number = 0

    for port in flags.auth_host_port:
        port_number = port
        try:
            httpd = ClientRedirectServer(
                (hostname, port),
                ClientRedirectHandler
            )

        except socket.error:
            pass
        else:
            success = True
            break


    if success:
        oauth_callback = 'http://{host}:{port}/'.format(
            host=flags.auth_host_name, port=port_number
        )
    else:
        oauth_callback = client.OOB_CALLBACK_URN

    flow.redirect_uri = oauth_callback
    authorize_url = flow.step1_get_authorize_url()

    if success:
        import webbrowser
        webbrowser.open(authorize_url, new=1, autoraise=True)
        #print(_BROWSER_OPENED_MESSAGE.format(address=authorize_url))
    else:
        pass
        #print(_GO_TO_LINK_MESSAGE.format(address=authorize_url))

    code = None

    if success:
        httpd.handle_request()

        if 'error' in httpd.query_params:
            sys.exit('Authentication request was rejected.')
        if 'code' in httpd.query_params:
            code = httpd.query_params['code']
        else:
            print('Failed to find "code" in the query parameters '
                  'of the redirect.')
            sys.exit('Try running with --noauth_local_webserver.')
    else:
        code = input('Enter verification code: ').strip()

    try:
        credential = flow.step2_exchange(code, http=http)
        print("CREDS", credential)
        print(help(credential))

    except client.FlowExchangeError as e:
        sys.exit('Authentication has failed: {0}'.format(e))

    storage.put(credential)
    credential.set_store(storage)
    print('Authentication successful.')

    return credential


def makeMeeting(credential, time, date, room):
    credentials = credential
    print(1)
    http = credentials.authorize(httplib2.Http())
    print(2)
    service = discovery.build(
        'calendar', 'v3', http=http, cache_discovery=False
    )

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/google-apps/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    # e.g. 14:00
    displace = [int(x) for x in time.split(':')]
    displace = displace[0]*3600 + displace[1]*60

    # e.g. 2017-06-12
    yy, mm, dd = [int(x) for x in date.split('-')]
    start = datetime.datetime(yy, mm, dd)
    end = start + datetime.timedelta(seconds=displace)

    # 8 hour UTC displacement
    start_str = start.strftime('%Y-%m-%dT%H:%M:%S-08:00')
    end_str = end.strftime('%Y-%m-%dT%H:%M:%S-08:00')

    event = {
      'summary': 'meeting',
      'location': room,
      'description': 'meeting arranged by bookeyapp',
      'start': {
        'dateTime': start_str,
        'timeZone': 'Asia/Singapore',
      },
      'end': {
        'dateTime': end_str,
        'timeZone': 'Asia/Singapore',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events(
        ).insert(calendarId='primary', body=event
        ).execute()

    return event.get('htmlLink')
