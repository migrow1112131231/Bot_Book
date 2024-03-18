import os
import sys


def _get_part_text(text: str, start: int, page_size: int):
    text_page: str
    while text[start:(start+page_size)][-1] not in '.,!:;?':
        page_size -= 1
    text_page = text[start:(start+page_size)]
    try:
        if text[len(text_page)+start] in '.,!:;?;' or text[len(text_page)+start+1] in '.,!:;?;':
            text_page = text_page[:-2]
            while text_page[-1] not in '.,!:;?':
                text_page = text_page[:-1]
    except:
        pass

    return text_page, len(text_page)


def prepare_book(path: str, PAGE_SIZE: int):
    book: 'dict[int, str]' = {}
    n, start = 0, 0
    with open(file=path, mode='r', encoding='u8') as file:
        content = file.read()
        while start + 5 < len(content):
            n += 1
            s = _get_part_text(content, start, PAGE_SIZE)
            book[n] = s[0].lstrip()
            start += s[1]
    return book


book = prepare_book(os.path.join(os.getcwd(), 'services\\book.txt'), 1050)
