import json

import requests

HEADERS = {'Content-Type': 'application/json', 'format': 'pandas-records'}
URL = 'http://0.0.0.0:8080'


class Rest(object):

    @staticmethod
    def invoke_internal_app(url, **kwargs):
        """
        This will invoke the server from the internal app
        """
        result = requests.post(url=url, data=json.dumps(kwargs), headers=HEADERS)
        return json.loads(result.content)

    def get_book_by_title(self, title: str):
        """
        Get book data by title
        """
        return self.invoke_internal_app(url=f"{URL}/search_book_by_title", title=title)

    def review_book(self, title: str, rating: float, review: str):
        """
        Use this to send a review for a book
        """
        return self.invoke_internal_app(url=f"{URL}/review_book", title=title, rating=rating, review=review)

    def get_details_from_specific_book(self, title: str):
        """
        Get all details from a specific book
        """
        return self.invoke_internal_app(url=f"{URL}/get_details_from_specific_book", title=title)

    def get_average_rating_per_month(self, title: str):
        """
        Get average rating of a book per month
        """
        return self.invoke_internal_app(url=f"{URL}/get_average_rating_per_month", title=title)

    def get_top_n_books(self, n: int):
        """
        Get the top n best rated books
        """
        return self.invoke_internal_app(url=f"{URL}/get_top_n_books", n=n)
