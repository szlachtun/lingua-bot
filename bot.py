import telebot
import configure
from keyboard import Keyboard
from dataclasses import dataclass

client = telebot.TeleBot(configure.config['token'])


# TODO: polish and german replacer
@dataclass
class Translation:
    def __init__(self):
        self.source_lang_abb: str = ''
        self.source_lang_abb: str = ''
        self.source_lang_name: str = ''
        self.target_lang_abb: str = ''
        self.target_lang_name: str = ''
        self.translate_query_human: str = ''
        self.translate_query_raw: str = ''
        self.translation_url: str = ''


@dataclass
class BablaVars:
    langs = {'pl': {'pl': 'polski', 'en': 'angielski', 'de': 'niemiecki', 'ru': 'rosyjski'},
             'en': {'pl': 'polish', 'en': 'english', 'de': 'german', 'ru': 'russian'},
             'de': {'pl': 'polnisch', 'en': 'english', 'de': 'deutsch', 'ru': 'russisch'},
             'ru': {'pl': 'польский', 'en': 'английский', 'de': 'немецкий', 'ru': 'русский'}}
    dic = {'pl': 'slownik', 'de': 'woerterbuch', 'en': 'dictionary'}


query = Translation()


class Handler:
    class General:
        @staticmethod
        def mode_setup(message):
            if message.text == 'Translate word':
                client.send_message(message.chat.id,
                                    '<strong>Enter source translation language</strong>',
                                    reply_markup=Keyboard.General.translation_setup(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.Word.source_lang_setup)

            elif message.text == 'Translate text':
                client.send_message(message.chat.id,
                                    '<strong>Enter source translation language</strong>',
                                    reply_markup=Keyboard.General.translation_setup(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, text_src_input)

            elif message.text == 'Meaning':
                client.send_message(message.chat.id,
                                    '<strong>From which language word you need to mean?</strong>',
                                    reply_markup=Keyboard.General.meaning_setup(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, mean_lang_input)

            elif message.text == '❌ Go back':
                client.send_message(message.chat.id,
                                    'How can I help you?',
                                    reply_markup=Keyboard.General.main(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.General.mode_setup)

            else:
                client.send_message(message.chat.id,
                                    '<strong>I don\'t know that :(</strong>',
                                    reply_markup=Keyboard.General.main(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.General.mode_setup)

    class Word:
        @staticmethod
        def source_lang_setup(message):
            global query
            if message.text == '❌ Go back':
                client.send_message(message.chat.id,
                                    'How can I help you?',
                                    reply_markup=Keyboard.General.main(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.General.mode_setup)
            elif message.text in Keyboard.emojis:
                query.source_lang_abb = message.text.split(' ')[1].lower()
                query.source_lang_name = BablaVars.langs[query.source_lang_abb][query.source_lang_abb]
                print(query.source_lang_abb, query.source_lang_name)

                client.send_message(message.chat.id,
                                    '<strong>Enter target translation language</strong>',
                                    reply_markup=Keyboard.General.translation_setup(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.Word.target_lang_setup)
            else:
                client.send_message(message.chat.id,
                                    '<strong>I don\'t know that :(</strong>',
                                    reply_markup=Keyboard.General.main(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.General.mode_setup)

        @staticmethod
        def target_lang_setup(message):
            global query
            if message.text == '❌ Go back':
                client.send_message(message.chat.id,
                                    'How can I help you?',
                                    reply_markup=Keyboard.General.main(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.General.mode_setup)
            elif message.text in Keyboard.emojis:
                query.target_lang_abb = message.text.split(' ')[1].lower()
                query.target_lang_name = BablaVars.langs[query.target_lang_abb][query.target_lang_abb]
                print(query.target_lang_abb, query.target_lang_abb)

                if query.target_lang_abb == query.source_lang_abb:
                    client.send_message(message.chat.id,
                                        'You\'ve chosen same source and target lang. Select source language:',
                                        reply_markup=Keyboard.General.translation_setup(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Word.source_lang_setup)
                else:
                    client.send_message(message.chat.id,
                                        '<strong>Enter word to translate</strong>',
                                        reply_markup=Keyboard.General.undo(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Word.runtime)

            else:
                client.send_message(message.chat.id,
                                    '<strong>I don\'t know that :(</strong>',
                                    reply_markup=Keyboard.General.main(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.General.mode_setup)

        @staticmethod
        def runtime(message):
            global query
            if message.text in ['❌ Go back', 'Try as text', 'Switch langs', 'Go to text mode', 'Get URL']:
                if message.text == '❌ Go back':
                    client.send_message(message.chat.id,
                                        'How can I help you?',
                                        reply_markup=Keyboard.General.main(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.General.mode_setup)
                elif message.text == 'Try as text':
                    pass
                elif message.text == 'Switch langs':
                    query.source_lang_abb, query.target_lang_abb = query.target_lang_abb, query.source_lang_abb
                    query.source_lang_name = BablaVars.langs[query.source_lang_abb][query.source_lang_abb]
                    query.target_lang_name = BablaVars.langs[query.target_lang_abb][query.target_lang_abb]
                    client.send_message(message.chat.id,
                                        f'Switched to {Keyboard.abb_to_emoji[query.source_lang_abb]} → '
                                        f'{Keyboard.abb_to_emoji[query.target_lang_abb]}',
                                        reply_markup=Keyboard.Word.runtime(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Word.runtime)
                elif message.text == 'Go to text mode':
                    pass
                elif message.text == 'Get URL':
                    client.send_message(message.chat.id,
                                        query.translation_url,
                                        reply_markup=Keyboard.Word.runtime(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Word.runtime)
            else:
                from parse import Parse
                query.translate_query_human = message.text
                Parse.translate(query)
                client.send_message(message.chat.id,
                                    query.translation_url,
                                    reply_markup=Keyboard.Word.runtime(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.Word.runtime)


@client.message_handler(commands=['start'])
def start(message):
    client.send_message(
        message.chat.id,
        'How can I help you?',
        reply_markup=Keyboard.General.main(),
        parse_mode='HTML')
    client.register_next_step_handler(message, Handler.General.mode_setup)


if __name__ == '__main__':
    client.polling(none_stop=True, interval=0)
