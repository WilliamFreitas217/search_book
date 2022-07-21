import json
import requests
from .constants import GUTENDEX_URL, BOOK_PARAMS


def invoke_gutendex(**kwargs):
    """
    This function will be used to get data from the gutendex
    """
    url_details = ''
    for k, v in kwargs.items():
        url_details += f"{k}={v}&"
    url_details = url_details[:-1]
    result = requests.post(GUTENDEX_URL + url_details)
    return json.loads(result.content)


def get_book_data(title: str):
    """
    Get the book data from gutendex
    :param title: book title
    :return: dictionary with all the collected data
    """
    all_results_raw = invoke_gutendex(title=title)
    results = all_results_raw['results']

    book = {}
    for b in results:
        if title.lower() == b['title'].lower():
            book = b
            break
    data = {}
    if book:
        for k, v in book.items():
            if k in BOOK_PARAMS:
                data[k] = v
    return data


def get_book_by_id(id: str):
    """
    Get book data from gutendex by id
    :param id: book id
    :return: dictionary containing the book data
    """
    all_results_raw = invoke_gutendex(id=id)

    results = all_results_raw['results']

    for b in results:
        if int(id) == b['id']:
            return b
    return {}
