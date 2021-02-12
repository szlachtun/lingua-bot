import telebot
import configure
import parse
from telebot import types

client = telebot.TeleBot(configure.config['token'])

langs = {'pl': {'pl': 'polski', 'en': 'angielski', 'de': 'niemiecki', 'ru': 'rosyjski'},
         'en': {'pl': 'polish', 'en': 'english', 'de': 'german', 'ru': 'russian'},
         'de': {'pl': 'polnisch', 'en': 'english', 'de': 'deutsch', 'ru': 'russisch'},
         'ru': {'pl': 'польский', 'en': 'английский', 'de': 'немецкий', 'ru': 'русский'}}

dic = {'pl': 'slownik', 'de': 'woerterbuch', 'en': 'dictionary'}
pol = {'ę': '%C4%99', 'ł': '%C5%82', 'ż': '%C5%BC', 'ó': '%C3%B3', 'ą': '%C4%85',
       'ć': '%C4%87', 'ź': '%C5%BA', 'ś': '%C5%9B', 'ń': '%C5%84', ' ': '-'}

goog = {'ę': '%C4%99', 'ł': '%C5%82', 'ż': '%C5%BC', 'ó': '%C3%B3', 'ą': '%C4%85',
        'ć': '%C4%87', 'ź': '%C5%BA', 'ś': '%C5%9B', 'ń': '%C5%84', ' ': '+'}

emoji = {'pl': '🇵🇱', 'en': '🇺🇸', 'de': '🇩🇪', 'ru': '🇷🇺'}

# IDEA: MOVE VARIABLES TO SEPARATE CLASS LIKE IN 'test.py'

tran_word = ''
begining = ''
ending = ''
src_lang = ''
trg_lang = ''
tr_word = ''
url = ''


@client.message_handler(commands=['start'])
def send_welcome(message):
    client.send_message(
        message.chat.id,
        '<i><strong>How can I help you?</strong></i>',
        reply_markup=Keyboard.main_keyboard(),
        parse_mode='HTML')
    client.register_next_step_handler(message, get_mode)


# @client.message_handler(content_types=['text'])
def get_mode(message):
    if message.text == 'Translate word':
        client.send_message(message.chat.id, '<strong>Enter source translation language</strong>',
                            reply_markup=Keyboard.translate_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, word_src_input)

    elif message.text == 'Translate text':
        client.send_message(message.chat.id, '<strong>Enter source translation language</strong>',
                            reply_markup=Keyboard.translate_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, text_src_input)

    elif message.text == 'Meaning':
        client.send_message(message.chat.id, '<strong>From which language word you need to mean?</strong>',
                            reply_markup=Keyboard.meaning_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, mean_lang_input)

    elif message.text == '❌ Go back':
        client.send_message(message.chat.id, '<i><strong>How can I help you?</strong></i>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)

    else:
        client.send_message(message.chat.id, '<strong>I don\'t know that :(</strong>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)


def word_src_input(message):
    global begining, src_lang
    if message.text == '❌ Go back':
        client.send_message(message.chat.id, '<i><strong>How can I help you?</strong></i>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)

    else:
        if message.text == '🇵🇱 PL' or message.text == '🇺🇸 EN' or message.text == '🇩🇪 DE' or message.text == '🇷🇺 RU':
            message.text = message.text.split(' ')
            begining = message.text[1].lower()
            src_lang = langs[begining][begining]

            client.send_message(message.chat.id, '<strong>Enter target translation language</strong>',
                                reply_markup=Keyboard.translate_keyboard(), parse_mode='HTML')
            client.register_next_step_handler(message, word_trg_input)

        else:
            client.send_message(message.chat.id, '<strong>I don\'t know that :(</strong>',
                                reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
            client.register_next_step_handler(message, get_mode)


def word_trg_input(message):
    global begining, ending, trg_lang
    if message.text == '❌ Go back':
        client.send_message(message.chat.id, '<strong>How can I help you?</strong>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)

    else:
        if message.text == '🇵🇱 PL' or message.text == '🇺🇸 EN' or message.text == '🇩🇪 DE' or message.text == '🇷🇺 RU':
            message.text = message.text.split(' ')
            ending = message.text[1].lower()

            if ending == begining:
                client.send_message(message.chat.id,
                                    '<strong>The same langs had been detected. From which language word you need to mean?</strong>',
                                    reply_markup=Keyboard.translate_keyboard(), parse_mode='HTML')
                client.register_next_step_handler(message, word_src_input)

            else:
                trg_lang = langs[begining][ending]
                client.send_message(message.chat.id, '<strong>Enter word to translate</strong>',
                                    reply_markup=Keyboard.undo_keyboard(), parse_mode='HTML')
                client.register_next_step_handler(message, word_create_url)

        else:
            client.send_message(message.chat.id, '<strong>I don\'t know that :(</strong>', parse_mode='HTML',
                                reply_markup=Keyboard.main_keyboard())
            client.register_next_step_handler(message, get_mode)


def word_create_url(message):
    global begining, src_lang, trg_lang, tr_word, dic, url, ending
    # if message.text != 'Get URL' and message.text != '❌ Go back' and message.text != 'Try as text': tr_word = message.text

    if message.text == '❌ Go back':
        client.send_message(message.chat.id, '<i><strong>How can I help you?</strong></i>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)

    elif message.text == 'Try as text':
        text = text_one_time(begining, ending, tr_word)
        client.send_message(message.chat.id, f'{text}', reply_markup=Keyboard.word_runtime_keyboard(),
                            parse_mode='HTML')
        client.register_next_step_handler(message, word_create_url)

    elif message.text == 'Switch langs':
        begining, ending = ending, begining

        src_lang = langs[begining][begining]
        trg_lang = langs[begining][ending]

        client.send_message(message.chat.id,
                            f'<strong>Switched to {emoji[begining]}{begining.upper()} → {emoji[ending]}{ending.upper()}</strong>',
                            reply_markup=Keyboard.word_runtime_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, word_create_url)

    elif message.text == 'Go to text mode':
        client.send_message(message.chat.id, f'<strong>Switched to text mode</strong>',
                            reply_markup=Keyboard.text_runtime_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, text_create_url)

    elif message.text == 'Get URL':
        for i in pol: tran_word = tr_word.replace(i, pol[i])

        if begining == 'ru':
            url = f'https://www.babla.ru/{src_lang}-{trg_lang}/{tr_word}'
        else:
            url = f'https://{begining}.bab.la/{dic[begining]}/{src_lang}-{trg_lang}/{tran_word}'

        client.send_message(message.chat.id, f'<strong><u>Keep your URL: {url}</u></strong>',
                            reply_markup=Keyboard.word_runtime_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, word_create_url)

    else:
        tr_word = message.text
        for i in pol: tran_word = tr_word.replace(i, pol[i])

        if begining == 'ru':
            url = f'https://www.babla.ru/{src_lang}-{trg_lang}/{tran_word}'
        else:
            url = f'https://{begining}.bab.la/{dic[begining]}/{src_lang}-{trg_lang}/{tran_word}'

        print(url)

        for i in range(3):
            text = parse.babla_parser(url)
            if text == []:
                if 0 <= i <= 1:
                    continue
                else:
                    if len(tr_word) >= 4:
                        tran_word = tr_word[4:]
                        for i in pol: tran_word = tr_word.replace(i, pol[i])
                        text = parse.babla_parser(url)

                        if text == []:
                            client.send_message(message.chat.id, '<strong>There is some error :(</strong>\n',
                                                reply_markup=Keyboard.word_error_keyboard(), parse_mode='HTML')
                            client.register_next_step_handler(message, word_create_url)
                            break

            elif text == ['Babla felled :(']:
                client.send_message(message.chat.id, '<strong>Babla felled :(</strong>\n',
                                    reply_markup=Keyboard.word_error_keyboard(), parse_mode='HTML')
                client.register_next_step_handler(message, word_create_url)
                break
            else:
                text = parse.babla_create_text(begining, ending, tr_word, text)
                client.send_message(message.chat.id, text, reply_markup=Keyboard.word_runtime_keyboard(),
                                    parse_mode='HTML')
                client.register_next_step_handler(message, word_create_url)
                break


def text_src_input(message):
    global begining

    if message.text == '🇵🇱 PL' or message.text == '🇺🇸 EN' or message.text == '🇩🇪 DE' or message.text == '🇷🇺 RU':
        begining = message.text.split(' ')[1].lower()
        client.send_message(message.chat.id, '<strong>Enter target translation language</strong>',
                            reply_markup=Keyboard.translate_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, text_trg_input)

    elif message.text == '❌ Go back':
        client.send_message(message.chat.id, '<i><strong>How can I help you?</strong></i>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)

    else:
        client.send_message(message.chat.id, '<strong>I don\'t know that :(', reply_markup=Keyboard.main_keyboard(),
                            parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)


def text_trg_input(message):
    global begining, ending

    if message.text == '🇵🇱 PL' or message.text == '🇺🇸 EN' or message.text == '🇩🇪 DE' or message.text == '🇷🇺 RU':
        ending = message.text.split(' ')[1].lower()

        if begining == ending:
            client.send_message(message.chat.id,
                                '<strong>The same langs had been detected. Enter source translation language</strong>',
                                reply_markup=Keyboard.translate_keyboard(), parse_mode='HTML')
            client.register_next_step_handler(message, text_src_input)

        else:
            client.send_message(message.chat.id, '<strong>Enter your text</strong>',
                                reply_markup=Keyboard.undo_keyboard(), parse_mode='HTML')
            client.register_next_step_handler(message, text_create_url)

    elif message.text == '❌ Go back':
        client.send_message(message.chat.id, '<i><strong>How can I help you?</strong></i>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)

    else:
        client.send_message(message.chat.id, '<strong>I don\'t know that :(</strong>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)


def text_create_url(message):
    global begining, ending, tr_word, url, src_lang, trg_lang
    if message.text != 'Get URL' and message.text != '❌ Go back' and message.text != 'Switch langs':
        tr_word = message.text

    if message.text == '❌ Go back':
        client.send_message(message.chat.id, '<i><strong>How can I help you?</strong></i>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)

    elif message.text == 'Get URL':
        client.send_message(message.chat.id, f'{url}', reply_markup=Keyboard.text_runtime_keyboard())
        client.register_next_step_handler(message, text_create_url)

    elif message.text == 'Switch langs':
        begining, ending = ending, begining
        client.send_message(message.chat.id,
                            f'<strong>Switched to {emoji[begining]}{begining.upper()} → {emoji[ending]}{ending.upper()}</strong>',
                            reply_markup=Keyboard.text_runtime_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, text_create_url)

    elif message.text == 'Go to word mode':
        client.send_message(message.chat.id, f'<strong>Switched to word mode</strong>',
                            reply_markup=Keyboard.word_runtime_keyboard(), parse_mode='HTML')
        begining == begining.lower()

        src_lang = langs[begining][begining]
        trg_lang = langs[begining][ending]

        client.register_next_step_handler(message, word_create_url)


    else:
        tran_word = tr_word.replace(' ', '+').replace('"', '\'')
        url = f'https://translate.google.com/m?sl={begining}&tl={ending}&q={tran_word}'
        text = f'<u><strong>Text translation</strong></u> ({parse.emoji[begining]}{begining.upper()} → {parse.emoji[ending]}{ending.upper()})\n'
        text += parse.google_parser(url)

        client.send_message(message.chat.id, f'{text}', reply_markup=Keyboard.text_runtime_keyboard(),
                            parse_mode='HTML')
        client.register_next_step_handler(message, text_create_url)


def text_one_time(begining, ending, tr_word):
    tran_word = tr_word.replace(' ', '+').replace('"', '\'')
    url = f'https://translate.google.com/m?sl={begining}&tl={ending}&q={tran_word}'
    text = f'<u><strong>Text translation</strong></u> ({parse.emoji[begining]}{begining.upper()} → {parse.emoji[ending]}{ending.upper()})\n'
    text += parse.google_parser(url)
    return text


def mean_lang_input(message):
    if message.text == '❌ Go back':
        client.send_message(message.chat.id, '<i><strong>How can I help you?</strong></i>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)

    elif message.text == '🇵🇱 PL':
        client.send_message(message.chat.id, '<strong>Write your word to explain</strong>',
                            reply_markup=Keyboard.undo_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, mean_create_url)


def mean_create_url(message):
    global src_lang, tr_word, url
    if message.text != 'Get URL' and message.text != '❌ Go back' and message.text != 'Synonims':
        tr_word = message.text.replace(' ', '%20')
        url = f'https://sjp.pwn.pl/szukaj/{tr_word}.html'

    if message.text == '❌ Go back':
        client.send_message(message.chat.id, '<i><strong>How can I help you?</strong></i>',
                            reply_markup=Keyboard.main_keyboard(), parse_mode='HTML')
        client.register_next_step_handler(message, get_mode)

    elif message.text == 'Get URL':
        client.send_message(message.chat.id, f'{url}', reply_markup=Keyboard.mean_runtime_keyboard())
        client.register_next_step_handler(message, mean_create_url)

    elif message.text == 'Synonims':
        pass

    else:
        text = parse.sjp_parser(url)
        text = parse.sjp_create_text(text)

        client.send_message(message.chat.id, f'{text}', reply_markup=Keyboard.mean_runtime_keyboard(),
                            parse_mode='HTML')
        client.register_next_step_handler(message, mean_create_url)


class Keyboard:
    @staticmethod
    def main_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

        btn1 = types.KeyboardButton('Translate word')
        markup.add(btn1)

        btn2 = types.KeyboardButton('Translate text')
        markup.add(btn2)

        btn3 = types.KeyboardButton('Meaning')
        markup.add(btn3)
        return markup

    @staticmethod
    def translate_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(row_width=2)

        btn1 = types.KeyboardButton('🇵🇱 PL')
        btn2 = types.KeyboardButton('🇺🇸 EN')
        markup.row(btn1, btn2)

        btn3 = types.KeyboardButton('🇩🇪 DE')
        btn4 = types.KeyboardButton('🇷🇺 RU')
        markup.row(btn3, btn4)

        btn5 = types.KeyboardButton('❌ Go back')
        markup.add(btn5)
        return markup

    @staticmethod
    def meaning_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(row_width=2)

        btn1 = types.KeyboardButton('🇵🇱 PL')
        markup.add(btn1)

        btn2 = types.KeyboardButton('❌ Go back')
        markup.add(btn2)
        return markup

    @staticmethod
    def word_runtime_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(row_width=2)
        btn1 = types.KeyboardButton('Get URL')
        markup.add(btn1)

        btn2 = types.KeyboardButton('Switch langs')
        btn3 = types.KeyboardButton('Go to text mode')
        markup.row(btn2, btn3)

        btn4 = types.KeyboardButton('❌ Go back')
        markup.add(btn4)
        return markup

    @staticmethod
    def word_error_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(row_width=2)

        btn2 = types.KeyboardButton('Try as text')
        btn3 = types.KeyboardButton('Get meaning')
        markup.row(btn2, btn3)

        btn4 = types.KeyboardButton('❌ Go back')
        markup.add(btn4)
        return markup

    @staticmethod
    def text_runtime_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(row_width=2)

        btn1 = types.KeyboardButton('Get URL')
        markup.add(btn1)

        btn2 = types.KeyboardButton('Switch langs')
        btn3 = types.KeyboardButton('Go to word mode')
        markup.row(btn2, btn3)

        btn4 = types.KeyboardButton('❌ Go back')
        markup.add(btn4)
        return markup

    @staticmethod
    def mean_runtime_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup = types.ReplyKeyboardMarkup(row_width=2)

        btn1 = types.KeyboardButton('Get URL')
        btn2 = types.KeyboardButton('Synonims')
        markup.row(btn1, btn2)

        btn3 = types.KeyboardButton('❌ Go back')
        markup.add(btn3)

    @staticmethod
    def undo_keyboard():
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        btn1 = types.KeyboardButton('❌ Go back')
        markup.add(btn1)
        return markup


if __name__ == '__main__':
    client.polling(none_stop=True, interval=0)
