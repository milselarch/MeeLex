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

def toDateTime(timeStr, dateStr):
    displace = [int(x) for x in timeStr.split(':')]
    displace = displace[0] * 3600 + displace[1] * 60

    # e.g. 2017-06-12
    yy, mm, dd = [int(x) for x in dateStr.split('-')]
    DT = datetime.datetime(yy, mm, dd)
    DT += datetime.timedelta(seconds=displace)
    return DT

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
    start = toDateTime(time, date)
    end = start + datetime.timedelta(seconds=3600)

    # 8 hour UTC displacement
    start_str = start.strftime('%Y-%m-%dT%H:%M:%S')
    end_str = end.strftime('%Y-%m-%dT%H:%M:%S')

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


def cheakIfFree(credential, start, end):
    http = credential.authorize(httplib2.Http())
    service = discovery.build(
        'calendar', 'v3', http=http, cache_discovery=False
    )

    #assuming both params are datetime objects
    start = start.isoformat() + "Z"
    end = end.isoformat() + "Z"

    print(start,end)
    eventsResult = service.events().list(
        calendarId='primary', timeMin=start, timeMax=end,
        maxResults=10, singleEvents=True, orderBy='startTime'
    ).execute()

    items = eventsResult['items']
    return items