import requests
from bs4 import BeautifulSoup

books = [
    {'url': 'https://www.kostenlosonlinelesen.net/kostenlose-samurai-1-der-weg-des-kaempfers-german-edition', 'pages': 101, 'path': './samurai/book_1/'},
    {'url': 'https://www.kostenlosonlinelesen.net/kostenlose-samurai-2-der-weg-des-schwertes-german-edition', 'pages': 111, 'path': './samurai/book_2/'},
    {'url': 'https://www.kostenlosonlinelesen.net/kostenlose-samurai-3-der-weg-des-drachen', 'pages': 135, 'path': './samurai/book_3/'},
    {'url': 'https://www.kostenlosonlinelesen.net/kostenlose-samurai-4-der-ring-der-erde-german-edition', 'pages': 99, 'path': './samurai/book_4/'},
    {'url': 'https://www.kostenlosonlinelesen.net/kostenlose-samurai-5-der-ring-des-wassers-german-edition', 'pages': 97, 'path': './samurai/book_5/'},
    {'url': 'https://www.kostenlosonlinelesen.net/kostenlose-samurai-6-der-ring-des-feuers-german-edition', 'pages': 101, 'path': './samurai/book_6/'},
    {'url': 'https://www.kostenlosonlinelesen.net/kostenlose-samurai-7-der-ring-des-windes-german-edition', 'pages': 116, 'path': './samurai/book_7/'}
]

def clean(text):
    text = text.replace('\xa0', '')
    text = text.replace('\r', '')
    text = text.replace('\n', '')
    text = text.replace('<br/>', '\n')
    text = text.strip()
    return text


for book in books:
    path = book['path']
    base_url = book['url']    
    for i in range(1, book['pages'] + 1):        
        if i == 1:
            url = base_url
        else:
            url = base_url + '/lesen/' + str(i)

        data_raw = requests.get(url)

        soup = BeautifulSoup(data_raw.text, 'html.parser')

        items = soup.find('div', {'class': 'inn cnt'}).contents[12:-4]

        items = [str(x) for x in items]

        text = clean(''.join(items))
        
        with open(path + str(i) + '.txt', 'w', encoding="utf-8") as f:
            f.write(text)
