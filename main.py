import logging
import os
import re

from googletrans import Translator
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def translate(update: Update, context: CallbackContext) -> None:
    if has_cyrillic(update.message.text):
        try:
            eng_message = translator.translate(update.message.text, dest="en").text
            update.message.reply_text(f"Would you please speak in English?\n\n{eng_message}")
        except Exception as e:
            logger.error(f"Exception during translate: {e}")


def main():
    updater = Updater(os.environ.get('TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    translator = Translator()
    main()
