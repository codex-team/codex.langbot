import logging
import os
import re

from googletrans import Translator
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext


def has_cyrillic(text):
    """
    Checking the text for the Cyrillic alphabet
    :param text: Text to check for Cyrillic
    """
    return bool(re.search('[а-яА-Я]', text))


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def is_photo(len):
    """
    Checking is message with photo
    :param len: Size of the photo tuple in the message
    :return: boolean value (True - message with photo, False - message without photo)
    """
    return bool(len)


def translate(update: Update, context: CallbackContext) -> None:
    """
    Translating message in telegram's chat with the Cyrillic
    """
    if is_photo(len(update.message.photo)):
        # Text in caption, because message with photo
        is_cyr = has_cyrillic(str(update.message.caption))
        mes = update.message.caption
    else:
        # Take text from message itself
        is_cyr = has_cyrillic(update.message.text)
        mes = update.message.text
    if is_cyr:
        try:
            # Translate message to English
            eng_message = translator.translate(mes, dest="en").text
            # Reply message with translated text
            update.message.reply_text(eng_message, quote=True)
        except Exception as e:
            logger.error(f"Exception during translate: {e}")


def main():
    # Initialize Update
    updater = Updater(os.environ.get('TOKEN'))
    dispatcher = updater.dispatcher
    # Add translating handler
    dispatcher.add_handler(MessageHandler((Filters.text | Filters.photo) & ~Filters.command, translate))
    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    translator = Translator()
    main()
