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
    if len(update.message.photo) != 0:
        is_cyr = has_cyrillic(str(update.message.caption))
        mes = update.message.caption
    else:
        is_cyr = has_cyrillic(update.message.text)
        mes = update.message.text
    if is_cyr:
        try:
            eng_message = translator.translate(mes, dest="en").text
            update.message.reply_text(eng_message, quote=True)
        except Exception as e:
            logger.error(f"Exception during translate: {e}")


def main():
    updater = Updater(os.environ.get('TOKEN'))
    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler((Filters.text | Filters.photo) & ~Filters.command, translate))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    translator = Translator()
    main()
