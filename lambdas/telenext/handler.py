import logging
import traceback

import json
import importlib

import os
import sys

try:
    here = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(os.path.join(here, "./lib"))
    sys.path.append(os.path.join(here, "../lib"))
    # https://docs.google.com/document/d/1WFQtcPc03D2fXwOAxg9ihwx-MqgTn0PYMleU-eI5g6k/edit?usp=sharing

    import newbot

except Exception as e:
    traceback.print_exc()

def process(event, context):
    print(event)

    rawTelegramData = event["body"]
    bot = newbot.lambdaBot()
    bot.dispatchRaw(rawTelegramData)

    return {
        "statusCode": 200,
        "body": "OK"
    }

def safeHandle(event, context):
    try:
        return process(event, context)
    except Exception as e:
        traceback.print_exc()

