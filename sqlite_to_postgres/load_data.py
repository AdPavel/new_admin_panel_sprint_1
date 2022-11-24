import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

import os
from dotenv import load_dotenv

from .extractor_saver import SQLiteExtractor, PostgresSaver

load_dotenv()
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
HOST = os.environ.get('HOST')
PORT = os.environ.get('PORT')


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)

if __name__ == '__main__':
    dsl = {'dbname': DB_NAME, 'user': DB_USER, 'password': DB_PASSWORD, 'host': HOST, 'port': PORT}
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
