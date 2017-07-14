# taken from https://developers.google.com/google-apps/calendar/quickstart/python
# python calender-test.py --noauth_local_webserver

import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import http.server as BaseHTTPServer

import datetime
import logging
import cAuth


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)

    print(credential_dir)
    credential_path = os.path.join(
        credential_dir, 'calendar-python-quickstart.json'
        )

    store = Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME

        print("FLAG PRE")

        if flags:
            print("TOOL RUN3", flags)
            #credentials = tools.run_flow(flow, store, flags)
            credentials = cAuth.run_flow(flow, store, 'localhost', 30001)

        else: # Needed only for compatibility with Python 2.6
            print("TOOL RUN2")
            credentials = tools.run(flow, store)

        print("AFTER TOOL")
        print('Storing credentials to ' + credential_path)

    return credentials

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    print("CREDENTIALS PRE")
    http = credentials.authorize(httplib2.Http())
    print("CREDENTIALS AFT")
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')

    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=10,
        singleEvents=True, orderBy='startTime'
    ).execute()

    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])


if __name__ == '__main__':
    main()