import json
import sys
from datetime import datetime

import pandas as pd
from flask import Flask, request

from .error_handling import InvalidAPIUsage
from .sqlite_connection import SQLConnection
from .utils import get_book_by_id, get_book_data

app = Flask(__name__)
sql = SQLConnection()


def verify_title(title):
    if not title:
        raise InvalidAPIUsage('The title is missing')


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return json.dumps(e.to_dict()), e.status_code


@app.route('/')
def server_online():
    return 'OK'


@app.route('/search_book_by_title', methods=['POST'])
def search_book_by_title():
    """
    Endpoint for searching the book by title
    """
    json_ = request.json
    title = json_['title']
    verify_title(title)
    return json.dumps(get_book_data(title))


@app.route('/review_book', methods=['POST'])
def review_book():
    """
    Endpoint for reviewing the book by title
    """
    json_ = request.json
    raw_data = [json_['title'], json_['rating'], json_['review']]

    details_raw = get_book_data(raw_data[0])
    if not all(raw_data):
        raise InvalidAPIUsage('There may be data missing')

    if not (0 <= raw_data[1] <= 5):
        raise InvalidAPIUsage('Rating Should have value between 0-5')

    data = pd.DataFrame({'book_id': [details_raw['id']],
                         'rating': [raw_data[1]],
                         'review': [raw_data[2]],
                         'month': [datetime.now().month]})

    try:
        data.to_sql('review', sql.get_db(), if_exists='append', index=False)
        return data.to_json()
    except Exception as e:
        return json.dumps({'result': f'error: {e}'})


@app.route('/get_details_from_specific_book', methods=['POST'])
def get_details_from_specific_book():
    """
    Get all details from a specific book, including rating average and reviews
    """
    json_ = request.json
    title = json_["title"]
    verify_title(title)

    details_raw = get_book_data(title)
    book_id = details_raw["id"]
    data = pd.read_sql(f'SELECT * FROM review WHERE book_id IN ({book_id})', sql.get_db())

    ratings = [float(v) for v in data['rating'].to_list()]
    average_rating = sum(ratings) / len(ratings)

    details_raw['rating'] = [average_rating]
    details_raw['reviews'] = data['review'].to_list()

    details_raw = {k: v if isinstance(v, list) and len(v) == 1 else [[v]] for k, v in details_raw.items()}
    data = pd.DataFrame(details_raw)
    return data.to_json()


@app.route('/get_average_rating_per_month', methods=['POST'])
def get_average_rating_per_month():
    """
    Gets average rating per month of a book
    """
    json_ = request.json
    title = json_["title"]
    verify_title(title)

    details_raw = get_book_data(json_["title"])
    book_id = details_raw["id"]
    data = pd.read_sql(f'SELECT * FROM review WHERE book_id IN ({book_id})', sql.get_db())

    data['rating'] = data['rating'].apply(lambda x: float(x))
    mean = data.groupby('month')['rating'].mean()

    return mean.to_json()


@app.route('/get_top_n_books', methods=['POST'])
def get_top_n_books():
    """
    Gets the top n books based on their rating
    """

    json_ = request.json
    n = int(json_["n"])
    if n <= 0:
        raise InvalidAPIUsage('The top n value must be greater than 0')

    data = pd.read_sql(f'SELECT * FROM review', sql.get_db())

    data['book_id'] = data['book_id'].apply(lambda x: get_book_by_id(id=x)['title'])
    data['rating'] = data['rating'].apply(lambda x: float(x))
    mean = data.groupby('book_id')['rating'].mean()

    return mean[:n].sort_values(ascending=False).to_json()


def main():
    app.run(host='0.0.0.0', port=8080 if len(sys.argv) < 2 else int(sys.argv[1]))
