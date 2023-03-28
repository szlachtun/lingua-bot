from bot import Translation
import requests
from bs4 import BeautifulSoup
from keyboard import Keyboard

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/87.0.4280.141 Safari/537.36'
}


class Parse:
    class Word:
        @staticmethod
        def make_url(obj: Translation):
            replace_rules = {'ę': '%C4%99', 'ł': '%C5%82', 'ż': '%C5%BC', 'ó': '%C3%B3', 'ą': '%C4%85',
                             'ć': '%C4%87', 'ź': '%C5%BA', 'ś': '%C5%9B', 'ń': '%C5%84', ' ': '+', 'Ä': '%C3%84',
                             'ä': '%C3%A4', 'Ö': '%C3%96', 'ö': '%C3%B6', 'Ü': '%C3%9C', 'ü': '%C3%BC',
                             'ẞ': '%E1%BA%9E',
                             'ß': '%C3%9F'}
            obj.translate_query_raw = ''
            for char in obj.translate_query_human:
                if char in replace_rules.keys():
                    obj.translate_query_raw += char.replace(char, replace_rules[char])
                else:
                    obj.translate_query_raw += char

            obj.translation_url = f"https://context.reverso.net/translation/{obj.source_lang_name}-" \
                                  f"{obj.target_lang_name}/{obj.translate_query_raw}"

        @staticmethod
        def translate(obj: Translation):
            Parse.Word.make_url(obj)
            print(obj.translation_url)

            try:
                obj.page_content = BeautifulSoup(requests.get(obj.translation_url, headers=headers).content,
                                                 'html.parser')
            except (ConnectionResetError, ConnectionResetError):
                print('pidory')
                exit()

            Parse.Word.reverso_parse(obj)
            Parse.Word.format(obj)

        @staticmethod
        def reverso_parse(obj: Translation):
            items = obj.page_content.find_all('span', {"class": "display-term"})
            words = []
            for item in items:
                if item != '\n':
                    words.append(item.get_text(strip=True))

            examples = obj.page_content.find_all("div", {"class": {"src ltr", "trg ltr"}})

            sentences = []
            for candidate in examples:
                couple = candidate.text.strip()
                sentences.append([couple])

            obj.result_word = words
            obj.result_sentence = sentences

        @staticmethod
        def format(obj: Translation):
            if len(obj.result_word) > 0:
                obj.result_message = f'<u><strong>{obj.translate_query_human}</strong></u> ' \
                                     f'({Keyboard.abb_to_emoji[obj.source_lang_abb]}{obj.source_lang_abb.upper()} → ' \
                                     f'{Keyboard.abb_to_emoji[obj.target_lang_abb]}{obj.target_lang_abb.upper()})\n'

                word_count = 5 if len(obj.result_word) > 5 else len(obj.result_word)
                for index in range(word_count):
                    obj.result_message += obj.result_word[index] + '\n'
            else:
                obj.result_message = f'Error\n'

    class Text:
        @staticmethod
        def make_url(obj: Translation):
            obj.translate_query_raw = obj.translate_query_human.replace(' ', '+').replace('"', '\'')
            obj.translation_url = f'https://translate.google.com/m?sl={obj.source_lang_abb}&tl={obj.target_lang_abb}' \
                                  f'&q={obj.translate_query_raw}'

        @staticmethod
        def gt_parse(obj: Translation):
            try:
                obj.page_content = BeautifulSoup(requests.get(obj.translation_url, headers=headers).content,
                                                 'html.parser')
            except (ConnectionResetError, ConnectionRefusedError):
                print("pidory")
            obj.result_sentence = obj.page_content.find('div', {'class': 'result-container'}).text
            obj.result_message = obj.result_sentence

        @staticmethod
        def translate(obj: Translation):
            Parse.Text.make_url(obj)
            Parse.Text.gt_parse(obj)
