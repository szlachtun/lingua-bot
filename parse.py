from bot import Translation
from bot import BablaVars


class Parse:
    @staticmethod
    def make_url(obj: Translation):
        replace_rules = {'ę': '%C4%99', 'ł': '%C5%82', 'ż': '%C5%BC', 'ó': '%C3%B3', 'ą': '%C4%85',
                         'ć': '%C4%87', 'ź': '%C5%BA', 'ś': '%C5%9B', 'ń': '%C5%84', ' ': '+', 'Ä': '%C3%84',
                         'ä': '%C3%A4', 'Ö': '%C3%96', 'ö': '%C3%B6', 'Ü': '%C3%9C', 'ü': '%C3%BC', 'ẞ': '%E1%BA%9E',
                         'ß': '%C3%9F'}
        obj.translate_query_raw = ''
        for char in obj.translate_query_human:
            if char in replace_rules.keys():
                obj.translate_query_raw += char.replace(char, replace_rules[char])
            else:
                obj.translate_query_raw += char

        if obj.source_lang_abb == 'ru':
            obj.translation_url = f"https://www.babla.ru/{obj.source_lang_name}-" \
                                  f"{obj.target_lang_name}/{obj.translate_query_raw}"
        else:
            obj.translation_url = f"https://{obj.source_lang_abb}.bab.la/{BablaVars.dic[obj.source_lang_abb]}" \
                                  f"/{obj.source_lang_name}-{obj.target_lang_name}/{obj.translate_query_raw}"

    @staticmethod
    def translate(obj: Translation):
        Parse.make_url(obj)
        print(obj.translation_url)
