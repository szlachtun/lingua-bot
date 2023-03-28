import telebot
import configure
from keyboard import Keyboard
from dataclasses import dataclass

client = telebot.TeleBot(configure.config['token'])


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
        self.page_content = None
        self.result_word: list = []
        self.result_sentence: list = []
        self.result_message: str = ''


query = Translation()
available_langs = {'pl': 'polish', 'en': 'english', 'de': 'german', 'ru': 'russian'}


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
                client.register_next_step_handler(message, Handler.Text.source_lang_setup)

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
                query.source_lang_name = available_langs[query.source_lang_abb]
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
                query.target_lang_name = available_langs[query.target_lang_abb]
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
                elif message.text == 'Switch langs':
                    query.source_lang_abb, query.target_lang_abb = query.target_lang_abb, query.source_lang_abb
                    query.source_lang_name = available_langs[query.source_lang_abb]
                    query.target_lang_name = available_langs[query.target_lang_abb]
                    client.send_message(message.chat.id,
                                        f'Switched to {Keyboard.abb_to_emoji[query.source_lang_abb]} → '
                                        f'{Keyboard.abb_to_emoji[query.target_lang_abb]}',
                                        reply_markup=Keyboard.Word.runtime(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Word.runtime)
                elif message.text == 'Go to text mode':
                    client.send_message(message.chat.id,
                                        'Switched to text mode',
                                        reply_markup=Keyboard.Text.runtime(),
                                        parse_mode='HTML')
                    query.source_lang_name = available_langs[query.source_lang_abb]
                    query.target_lang_name = available_langs[query.target_lang_abb]
                    client.register_next_step_handler(message, Handler.Text.runtime)
                elif message.text == 'Get URL':
                    client.send_message(message.chat.id,
                                        query.translation_url,
                                        reply_markup=Keyboard.Word.runtime(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Word.runtime)
            else:
                from parse import Parse
                query.translate_query_human = message.text
                Parse.Word.translate(query)
                client.send_message(message.chat.id,
                                    query.result_message,
                                    reply_markup=Keyboard.Word.runtime(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.Word.runtime)

    class Text:
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
                query.source_lang_name = available_langs[query.source_lang_abb]
                print(query.source_lang_abb, query.source_lang_name)

                client.send_message(message.chat.id,
                                    '<strong>Enter target translation language</strong>',
                                    reply_markup=Keyboard.General.translation_setup(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.Text.target_lang_setup)
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
                query.target_lang_name = available_langs[query.target_lang_abb]
                print(query.target_lang_abb, query.target_lang_abb)

                if query.target_lang_abb == query.source_lang_abb:
                    client.send_message(message.chat.id,
                                        'You\'ve chosen same source and target lang. Select source language:',
                                        reply_markup=Keyboard.General.translation_setup(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Text.source_lang_setup)
                else:
                    client.send_message(message.chat.id,
                                        '<strong>Enter word to translate</strong>',
                                        reply_markup=Keyboard.General.undo(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Text.runtime)

            else:
                client.send_message(message.chat.id,
                                    '<strong>I don\'t know that :(</strong>',
                                    reply_markup=Keyboard.General.main(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.General.mode_setup)

        @staticmethod
        def runtime(message):
            global query
            if message.text in ['❌ Go back', 'Switch langs', 'Go to word mode', 'Get URL']:
                if message.text == '❌ Go back':
                    client.send_message(message.chat.id,
                                        'How can I help you?',
                                        reply_markup=Keyboard.General.main(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.General.mode_setup)
                elif message.text == 'Switch langs':
                    query.source_lang_abb, query.target_lang_abb = query.target_lang_abb, query.source_lang_abb
                    query.source_lang_name = available_langs[query.source_lang_abb]
                    query.target_lang_name = available_langs[query.target_lang_abb]
                    client.send_message(message.chat.id,
                                        f'Switched to {Keyboard.abb_to_emoji[query.source_lang_abb]} → '
                                        f'{Keyboard.abb_to_emoji[query.target_lang_abb]}',
                                        reply_markup=Keyboard.Text.runtime(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Text.runtime)
                elif message.text == 'Go to word mode':
                    client.send_message(message.chat.id,
                                        'Switched to word mode',
                                        reply_markup=Keyboard.Word.runtime(),
                                        parse_mode='HTML')
                    query.source_lang_name = available_langs[query.source_lang_abb]
                    query.target_lang_name = available_langs[query.target_lang_abb]
                    client.register_next_step_handler(message, Handler.Word.runtime)
                elif message.text == 'Get URL':
                    client.send_message(message.chat.id,
                                        query.translation_url,
                                        reply_markup=Keyboard.Text.runtime(),
                                        parse_mode='HTML')
                    client.register_next_step_handler(message, Handler.Text.runtime)
            else:
                from parse import Parse
                query.translate_query_human = message.text
                Parse.Text.translate(query)
                client.send_message(message.chat.id,
                                    query.result_message,
                                    reply_markup=Keyboard.Text.runtime(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, Handler.Text.runtime)


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
