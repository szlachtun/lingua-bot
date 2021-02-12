import requests
from bs4 import BeautifulSoup

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'
}
emoji = {'pl': '🇵🇱', 'en': '🇺🇸', 'de': '🇩🇪', 'ru': '🇷🇺'}
text = ''
apo = "'"


def babla_parser(URL):
    global text
    try:
        r = requests.get(URL, headers=headers)
    except ConnectionError:
        text = 'Something wrong with your Internet connection'
        return text

    soup = BeautifulSoup(r.content, 'html.parser')
    print(soup)
    items = []
    try:
        raw = soup.find('div', {'class': {'quick-results', 'container'}})
        raw_items = raw.find_all('div', {'class': 'quick-result-entry'})
    except AttributeError:
        items = ['Babla felled :(']
        return items

    for raw_item in raw_items[:-1]:
        line = []

        try:
            line.append(raw_item.find('a', {'class': 'babQuickResult'}).text.strip())
        except AttributeError:
            try:
                line.append(raw_item.find('span', {'class': 'babQuickResult'}).text.strip())
            except AttributeError:
                items = ['Babla felled :(']
                return items

        data = raw_item.find('ul', {'class': 'sense-group-results'})
        if data.find_all('span') == []:
            right = data.find_all('a')
            for r in range(len(right)):
                right[r] = right[r].text
            line.append(right)
        else:
            right = data.find_all('span')
            for r in range(len(right)):
                right[r] = right[r].text
            line.append(right)
        items.append(line)

    return items


def babla_create_text(source, target, t_word, items):
    information = f'<u><strong>{t_word}</strong></u> ({emoji[source]}{source.upper()} → {emoji[target]}{target.upper()})\n'

    if len(items) > 4: items = items[:5]

    for item in items:
        line = f'<strong>{item[0]}</strong> — '
        if len(item[1]) > 4: item[1] = item[1][:5]
        for i in range(len(item[1])):
            line += f'{item[1][i].strip(apo)}, '

        line = line[:-2]
        line += '\n'
        information += line
    return information


def google_parser(URL):
    global text
    try:
        r = requests.get(URL, headers=headers)
    except ConnectionError:
        text = 'Something wrong with your Internet connection'
        return text

    soup = BeautifulSoup(r.content, 'html.parser')

    data = soup.find('div', {'class': 'result-container'}).text
    data = f'<a>{data}</a>'
    return data


def sjp_parser(URL):
    try:
        r = requests.get(URL, headers=headers)
    except ConnectionError:
        text = 'Something wrong with your Internet connection'
        return text

    soup = BeautifulSoup(r.content, 'html.parser')
    items = []

    site = soup.find_all('div', {'class': 'wyniki'})
    items.append([soup.find('div', {'class': 'query'}).text.title()])

    print(site)

    if site == []:
        items.append(['There is no meaning for this word :('])

    for block in range(len(site)):
        if block == 0:
            items.append([
                site[block].find('div', {'class': 'entry-body'}).get_text(strip=True)]
            )
        else:
            mean_data = site[block].find_all('div', {'class': 'znacz'})
            if mean_data == []:
                continue
            else:
                for mean in range(len(mean_data)): mean_data[mean] = ' ' + mean_data[mean].get_text(strip=True)

            items.append([
                site[block].find('span', {'class': 'tytul'}).get_text(strip=True), mean_data]
            )

    print(items)
    return items


def sjp_create_text(items):
    print(items)
    information = f'<u><strong>{items[0][0]}</strong></u> — Definicja\n'
    for item in range(1, len(items)):
        if item == 1:
            information += f'<i>{items[item][0]}</i>\n'
        else:
            information += f'<strong>{items[item][0]}</strong>\n'
            for mean in items[item][1]:
                information += f'<strong>{mean}</strong>\n'

    return information


'''url = 'https://translate.google.com/m?sl=en&tl=ru&q=Why+does+the+interviewer+think+what+Kate+says+is+refreshing'
google_parser(url)'''
'''data = sjp_parser('https://sjp.pwn.pl/szukaj/biurko.html')
print(sjp_create_text(data))'''
