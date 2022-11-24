import sqlite3


class PostgresSaver:
    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self):
        pass


class SQLiteExtractor:
    def __init__(self, conn):
        self.conn = conn

    def extract_movies(self):
        data = dict()
        self.conn.row_factory = sqlite3.Row
        curs = self.conn.cursor()
        curs.execute(f'SELECT name FROM sqlite_master WHERE type="table";')
        tables = curs.fetchall()
        for table in tables:
            table_name = dict(table)["name"]
            curs.execute(f'SELECT * FROM {table_name};')
            data[table_name] = list(map(dict, curs.fetchall()))
        return data
