import logging
import traceback

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
    )

try:
    import json
    import importlib

    cAuth = importlib.import_module("cAuth")
    dynamo = importlib.import_module("dynamo")

    # https://docs.google.com/document/d/1WFQtcPc03D2fXwOAxg9ihwx-MqgTn0PYMleU-eI5g6k/edit?usp=sharing



    def respond(event, context):
        """
        # Use this code if you don't use the http event
        # with the LAMBDA-PROXY integration
        return {
            "message": "Go Serverless v1.0! function execute success!",
            "event": event
        }
        """

        body = {
            "message": "Go Serverless v1.0! Function execute success!",
            "input": event
            # "input": event
        }

        params = event["queryStringParameters"]
        telegram_id = params["state"]
        code = params["code"]

        flow = cAuth.JsonToFlow(dynamo.readFlow(telegram_id))
        credential = cAuth.authHandleCode(flow, code)
        dynamo.addCredential(telegram_id, credential.to_json())

        return {
            "statusCode": 200,
            "body": json.dumps(code),
            "message": "You have been authenticated!"
        }

except:
    logging.error(traceback.format_exc())