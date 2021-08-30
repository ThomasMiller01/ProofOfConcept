import os

books = [
    # './samurai/book_1',
    # './samurai/book_2',
    './samurai/book_3',
    './samurai/book_4',
    './samurai/book_5',
    './samurai/book_6',
    './samurai/book_7'    
]

for book in books:
    total = []
    
    items = []

    for root, dirs, files in os.walk(book):
        for name in files:
            if 'all' not in name:
                items.append(root + '/' + name)
    
    items.sort(key=lambda elem: int(elem.split('/')[-1].split('.')[0]))

    for item in items:
        with open(item, 'r', encoding="utf-8") as f:
            content = f.readlines()
            total.append(''.join(content))

    total_text = ' '.join(total)

    with open('./samurai/books/' + book.split('/')[-1] + '.txt', 'w', encoding="utf-8") as f:
        f.write(total_text)    