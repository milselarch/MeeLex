from telegram.ext import Updater
from telegram.ext import CommandHandler

import logging
import dynamo
import cAuth

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

    def start(self):
        self.updater.start_polling()

    def chatStart(self, bot, update):
        #logging.log(logging.INFO, bot, (update,))
        #message.from_user.id
        print(update.message.from_user.id)
        telegram_id = update.message.from_user.id

        oAuths = dynamo.read(telegram_id)
        print("OAUTHS: " + str(oAuths))
        reply = Reply(bot, update.message.chat_id)

        if oAuths == []:
            link, httpd, flow = cAuth.makeAuthLink("localhost", 30001)

            reply.send("please authenticate at " + link)
            credential = cAuth.authHandleRequest(flow, httpd)
            dynamo.insert(telegram_id, credential.to_json())
            reply.send("Calander API linked your Telegram!")

        else:
            reply.send("You have been authenticated already")

    def chatRepeat(self, bot, update, args):
        logging.log(logging.INFO, bot, (update, args))

        bot.sendMessage(
            chat_id=update.message.chat_id,text=args
        )


if __name__ == '__main__':
    toaster = ToastParser()
    toaster.start()