from telegram.ext import Updater
from telegram.ext import CommandHandler

import logging
import dynamo
import lexmel
import cAuth
import json

import threading

import authServer
authServer.run(threaded=True)

import config
conf = config.config()

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
    )

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

    def start(self):
        self.updater.start_polling()

    def authenticate(self, replyObj, user_id):
        link, httpd, flow = cAuth.makeAuthLink("localhost", 30001)
        replyObj.send("please authenticate at " + link)
        credential = cAuth.authHandleRequest(flow, httpd)
        dynamo.insert(user_id, credential.to_json())
        replyObj.send("Calander API linked your Telegram!")

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
                reply("Authentication process failed!!")

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
        lexUser = None

        if telegram_id in lexmel.users:
            print("I!1")
            lexUser = lexmel.users[telegram_id]

        else:
            print("IE!2")
            oAuths = dynamo.read(telegram_id)

            if oAuths != []:
                print("OLD OAUTH")
                lexmel.users[telegram_id] = lexmel.state(telegram_id)
                lexUser = lexmel.users[telegram_id]
                print("END OLD OAUTH")

            else:
                print("NEW OAUTH")

                try:
                    self.authenticate(reply, telegram_id)
                    lexmel.users[telegram_id] = lexmel.state(telegram_id)
                    lexUser = lexmel.users[telegram_id]

                except (ValueError, cAuth.client.FlowExchangeError) as e:
                    reply("Authentication process failed!!")

        print("LEX USER", lexUser)

        if lexUser != None:
            print("N!1")
            print("LEX-RES", args)
            lexResponse = lexUser.send(inText)

            #print(json.dumps(lexResponse, indent=4, sort_keys=True))

            if "message" in lexResponse:
                reply.send(lexResponse["message"])


if __name__ == '__main__':
    toaster = ToastParser()
    toaster.start()