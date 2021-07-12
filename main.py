#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


import os
import time

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackContext

from config import TOKEN
from common import get_logger, log_func, reply_error
from third_party import zalgo


log = get_logger(__file__)


@log_func(log)
def on_start(update: Update, context: CallbackContext):
    update.message.reply_text(
        'Enter something and the bot will return it as Z̗̱̥̝̔̑ͯͬ̈̍̊Ḁ̪̬̟̾L̗̺̞̎̑͑̑̄̓G͎̰̞̯O̹̹ text'
    )


@log_func(log)
def on_request(update: Update, context: CallbackContext):
    message = update.effective_message

    message.reply_text(
        zalgo.he_comes(message.text),
        quote=True
    )


def on_error(update: Update, context: CallbackContext):
    reply_error(log, update, context)


def main():
    cpu_count = os.cpu_count()
    workers = cpu_count
    log.debug('System: CPU_COUNT=%s, WORKERS=%s', cpu_count, workers)

    log.debug('Start')

    updater = Updater(
        TOKEN,
        workers=workers,
        use_context=True
    )

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', on_start, run_async=True))
    dp.add_handler(MessageHandler(Filters.text, on_request, run_async=True))

    dp.add_error_handler(on_error)

    updater.start_polling()
    updater.idle()

    log.debug('Finish')


if __name__ == '__main__':
    while True:
        try:
            main()
        except:
            log.exception('')

            timeout = 15
            log.info(f'Restarting the bot after {timeout} seconds')
            time.sleep(timeout)
