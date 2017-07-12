from telegram.ext import Updater
from telegram.ext import CommandHandler

import logging

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
            'reply', self.reply, pass_args=True
        ))

    def start(self):
        self.updater.start_polling()

    def reply(self, bot, update, args):
        logging.log(logging.INFO, bot, (update, args))

        bot.sendMessage(
            chat_id=update.message.chat_id, text=args
        )

if __name__ == '__main__':
    toaster = ToastParser()
    toaster.start()