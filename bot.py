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
        if oAuths == []:
            link, httpd, flow = cAuth.makeAuthLink("localhost", 30001)

            text = "please authenticate at " + link
            bot.sendMessage(
                chat_id=update.message.chat_id, text=text
            )

            cAuth.authHandleRequest(flow, httpd)

    def chatRepeat(self, bot, update, args):
        logging.log(logging.INFO, bot, (update, args))

        bot.sendMessage(
            chat_id=update.message.chat_id, text=args
        )


if __name__ == '__main__':
    toaster = ToastParser()
    toaster.start()