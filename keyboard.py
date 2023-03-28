from telebot import types

class Keyboard:
    class General:
        @staticmethod
        def main():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

            btn1 = types.KeyboardButton('Translate word')
            markup.add(btn1)

            btn2 = types.KeyboardButton('Translate text')
            markup.add(btn2)

            btn3 = types.KeyboardButton('Meaning')
            markup.add(btn3)
            return markup

        @staticmethod
        def translation_setup():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)

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
        def meaning_setup():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)

            btn1 = types.KeyboardButton('🇵🇱 PL')
            markup.add(btn1)

            btn2 = types.KeyboardButton('❌ Go back')
            markup.add(btn2)
            return markup

        @staticmethod
        def undo():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            btn1 = types.KeyboardButton('❌ Go back')
            markup.add(btn1)
            return markup

    class Word:
        @staticmethod
        def runtime():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton('Get URL')
            markup.add(btn1)

            btn2 = types.KeyboardButton('Switch langs')
            btn3 = types.KeyboardButton('Go to text mode')
            markup.row(btn2, btn3)

            btn4 = types.KeyboardButton('❌ Go back')
            markup.add(btn4)
            return markup

        @staticmethod
        def error():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)

            btn2 = types.KeyboardButton('Try as text')
            btn3 = types.KeyboardButton('Get meaning')
            markup.row(btn2, btn3)

            btn4 = types.KeyboardButton('❌ Go back')
            markup.add(btn4)
            return markup

    class Text:
        @staticmethod
        def runtime():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)

            btn1 = types.KeyboardButton('Get URL')
            markup.add(btn1)

            btn2 = types.KeyboardButton('Switch langs')
            btn3 = types.KeyboardButton('Go to word mode')
            markup.row(btn2, btn3)

            btn4 = types.KeyboardButton('❌ Go back')
            markup.add(btn4)
            return markup

    class Mean:
        @staticmethod
        def runtime():
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)

            btn1 = types.KeyboardButton('Get URL')
            btn2 = types.KeyboardButton('Synonyms')
            markup.row(btn1, btn2)

            btn3 = types.KeyboardButton('❌ Go back')
            markup.add(btn3)
