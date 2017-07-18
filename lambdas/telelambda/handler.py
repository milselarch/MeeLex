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

    import cAuth
    import dynamo

except Exception as e:
    traceback.print_exc()

def process(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps(event),
    }

def respond(event, context):
    try:
        return process(event, context)
    except Exception as e:
        traceback.print_exc()


