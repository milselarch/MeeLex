from telegram.ext import Updater
from telegram.ext import CommandHandler

import logging
import yaml
import time

class config(object):
    filename = ''

    def __init__(self):
        fileData = open(self.filename).read()
        fileData = fileData.replace('\t', ' ' * 4)
        self.data = yaml.load(fileData)

logging.basicConfig(
    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level = logging.INFO
    )

class ToastParser(object):
    toastToken = '389237665:AAHmX25t0ge5qo0hdd99DsUAvhD-l8v8q1s'

    def __init__(self):
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