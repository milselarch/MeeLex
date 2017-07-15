from telegram.ext import Updater
from telegram.ext import CommandHandler

import logging
import dynamo
import lexmel
#import calander
import cAuth
import json

import urllib.request

import authServer
authServer.run(threaded=True)

import config
conf = config.config()
authAddr = conf['authAddr']

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
    )

flows = {}

class Reply(object):
    def __init__(self, bot, chat_id):
        self.bot = bot
        self.chat_id = chat_id

    def send(self, text):
        self.bot.sendMessage(
            chat_id=self.chat_id,
            text=text
        )

class ToastParser(object):
    toastToken = conf['botToken']

    def __init__(self):
        print(self.toastToken)
        self.updater = Updater(self.toastToken)

        dispatcher = self.updater.dispatcher
        dispatcher.add_handler(CommandHandler(
            'start', self.chatStart, pass_args=False
        ))
        dispatcher.add_handler(CommandHandler(
            'repeat', self.chatRepeat, pass_args=True
        ))
        dispatcher.add_handler(CommandHandler(
            'bookApp', self.chatLex, pass_args=True
        ))
        dispatcher.add_handler(CommandHandler(
            'b', self.chatLex, pass_args=True
        ))
        dispatcher.add_handler(CommandHandler(
            'code', self.chatCode, pass_args=True
        ))

        dispatcher.add_handler(CommandHandler(
            'devc', self.chatDevc, pass_args=True
        ))

    def start(self):
        self.updater.start_polling()

    def authenticate(self, replyObj, user_id):
        #link, httpd, flow = cAuth.makeAuthLink("localhost", 30001)
        link, flow = cAuth.makeAuthLink()
        text = "please authenticate at " + link + "."
        text += " use /code <yourcode> to activate code"
        replyObj.send("please authenticate at " + link)

        flows[user_id] = flow

    def chatCode(self, bot, update, args):
        reply = Reply(bot, update.message.chat_id)
        telegram_id = update.message.from_user.id

        if len(args) == 0:
            reply.send("code is empty!")

        elif telegram_id in flows:
            flow = flows[telegram_id]
            code = args[0]

            try:
                credential = cAuth.authHandleCode(flow, code)
                dynamo.insert(telegram_id, credential.to_json())
                reply.send("Calander API linked your Telegram!")

                del flows[telegram_id]

            except cAuth.client.FlowExchangeError:
                reply.send("code is wrong, try again.")

        else:
            reply.send("you haven't started with setup using /start !")

    def chatStart(self, bot, update):
        #logging.log(logging.INFO, bot, (update,))
        #message.from_user.id
        print(update.message.from_user.id)
        telegram_id = update.message.from_user.id

        oAuths = dynamo.read(telegram_id)
        print("OAUTHS: " + str(oAuths))
        reply = Reply(bot, update.message.chat_id)

        if oAuths == []:
            try:
                self.authenticate(reply, telegram_id)
            except (ValueError, cAuth.client.FlowExchangeError) as e:
                logging.error(e)
                reply.send("Authentication process failed!!")

        else:
            reply.send("You have been authenticated already")

    def chatRepeat(self, bot, update, args):
        logging.log(logging.INFO, bot, (update, args))

        bot.sendMessage(
            chat_id=update.message.chat_id,text=args
        )

    def chatLex(self, bot, update, args):
        #logging.log(logging.INFO, bot, (update, str(args)))
        print("CHAT LEX")
        telegram_id = update.message.from_user.id
        reply = Reply(bot, update.message.chat_id)
        inText = " ".join(args)

        if (inText == ''): return

        print(inText, "INTEXT")
        print("IE!2")
        oAuths = dynamo.read(telegram_id)

        if oAuths == []:
            print("NEW OAUTH")

            try:
                self.authenticate(reply, telegram_id)
                lexmel.users[telegram_id] = lexmel.state(telegram_id)
                lexUser = lexmel.users[telegram_id]

            except (ValueError, cAuth.client.FlowExchangeError) as e:
                reply("Authentication process failed!!")
                return

        credentialJSON = oAuths[0]["credential"]
        credential = cAuth.makeCredential(credentialJSON)

        if telegram_id in lexmel.users:
            print("I!1")
            lexUser = lexmel.users[telegram_id]
        else:
            print("OLD OAUTH")
            lexmel.users[telegram_id] = lexmel.state(telegram_id)
            lexUser = lexmel.users[telegram_id]
            print("END OLD OAUTH")

        print("LEX USER", lexUser)
        print("N!1")
        print("LEX-RES", args)

        lexResponse = lexUser.send(inText)
        print(json.dumps(lexResponse, indent=4, sort_keys=True))

        if "message" in lexResponse:
            reply.send(lexResponse["message"])

        elif lexResponse["dialogState"] == "ReadyForFulfillment":
            """
            #example
            "slots": {
                "NumberOfPeople": "10",
                "RoomDate": "2017-07-15",
                "RoomNames": "yomama",
                "RoomTimeSlot": "14:00"
            }
            """

            slots = lexResponse["slots"]
            people = slots["NumberOfPeople"]
            roomDate = slots["RoomDate"]
            roomName = slots["RoomNames"]
            roomTimeSlot = slots["RoomTimeSlot"]

            link = cAuth.makeMeeting(
                credential, roomTimeSlot, roomDate, roomName
            )

            reply.send("Room booked! View details @ " + link)

    def chatDevc(self, bot, update, args):
        #logging.log(logging.INFO, bot, (update, str(args)))
        print("CHAT LEX")
        telegram_id = update.message.from_user.id
        reply = Reply(bot, update.message.chat_id)
        inText = " ".join(args)

        oAuths = dynamo.read(telegram_id)

        if oAuths != []:
            credentialJSON = oAuths[0]["credential"]
            credential = cAuth.makeCredential(credentialJSON)
            print("PRE MAKE MEET")

            meetingLink = cAuth.makeMeeting(
                credential, '14:21', '2017-09-21', 'da vinci'
            )

            reply.send("meeting scheduled. view at " + meetingLink)

        else:
            reply.send("SETUP CALANDER CREDENTIAL FIRST")


if __name__ == '__main__':
    toaster = ToastParser()
    toaster.start()