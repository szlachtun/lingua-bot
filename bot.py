import telebot
import configure
from keyboard import Keyboard
from dataclasses import dataclass

client = telebot.TeleBot(configure.config['token'])


# TODO: polish and german replacer
@dataclass
class Translation:
    def __init__(self):
        source_lang_abb: str
        source_lang_name: str
        target_lang_abb: str
        target_lang_name: str
        translate_query: str
        translation_url: str


@dataclass
class BablaVars:
    def __init__(self):
        langs = {'pl': {'pl': 'polski', 'en': 'angielski', 'de': 'niemiecki', 'ru': 'rosyjski'},
                 'en': {'pl': 'polish', 'en': 'english', 'de': 'german', 'ru': 'russian'},
                 'de': {'pl': 'polnisch', 'en': 'english', 'de': 'deutsch', 'ru': 'russisch'},
                 'ru': {'pl': 'польский', 'en': 'английский', 'de': 'немецкий', 'ru': 'русский'}}
        dic = {'pl': 'slownik', 'de': 'woerterbuch', 'en': 'dictionary'}


keyboard_emoji = {'pl': '🇵🇱', 'en': '🇺🇸', 'de': '🇩🇪', 'ru': '🇷🇺'}
babla = BablaVars


@client.message_handler(commands=['start'])
def send_welcome(message):
    client.send_message(
        message.chat.id,
        'Hello!',
        reply_markup=Keyboard.General.main(),
        parse_mode='HTML')
    client.register_next_step_handler(message, get_mode)


if __name__ == '__main__':
    client.polling(none_stop=True, interval=0)
