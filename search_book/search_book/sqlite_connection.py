import sqlite3
from pathlib import Path


class SQLConnection:
    """
    Class responsible for persist data

    """

    def __init__(self):
        self.database = Path().home() / '.search_book/'
        self.database.mkdir(exist_ok=True)
        self.database /= 'data.db'
        self.initiate_table()

    @staticmethod
    def get_table_params(columns):
        table_params = ""
        for c in columns:
            table_params += f"{c} text,"
        table_params = table_params[:-1]
        return table_params

    def execute(self, query, param=None):
        try:
            cur = self.get_db()
            if param:
                cur.execute(query, param)
            else:
                cur.execute(query)
            cur.commit()

        except sqlite3.Error as e:
            raise e

    def get_db(self):
        """
        Create database connection

        """
        conn = None
        try:
            conn = sqlite3.connect(self.database)
            return conn
        except sqlite3.Error as e:
            raise e
        return conn

    def query_db(self, query, args=(), one=False):
        """
        Create a query for database info retrieval

        :param query: database query.
        :return: cursor status.
        """
        cur = self.get_db().execute(query, args)
        rv = cur.fetchall()
        cur.close()

        return (rv[0] if rv else None) if one else rv

    def initiate_table(self):
        columns = ['book_id', 'rating', 'review', 'month']
        self.execute(f'CREATE TABLE IF NOT EXISTS review({self.get_table_params(columns)})')
