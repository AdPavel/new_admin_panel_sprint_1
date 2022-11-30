import sqlite3
import psycopg2

from contextlib import contextmanager
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from config import settings
from extractor_saver import SQLiteExtractor, PostgresSaver


@contextmanager
def conn_context_sqlite(db_path: str):
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        yield conn
    except sqlite3.Error as msg:
        print('Ошибка SQLlite: ', msg)
    finally:
        if conn:
            conn.close()


@contextmanager
def conn_context_pg(dsl):
    try:
        pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
        yield pg_conn
    except psycopg2.Error as msg:
        print('Ошибка PostGres: ', msg)
    finally:
        if pg_conn:
            pg_conn.close()



def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_extractor = SQLiteExtractor(connection)

    data = sqlite_extractor.extract_movies()
    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': settings.db_name, 'user': settings.db_user,
           'password': settings.db_password, 'host': settings.host,
           'port': settings.port}
    with conn_context_sqlite(settings.db_path) as sqlite_conn,\
            conn_context_pg(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
