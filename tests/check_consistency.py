import sqlite3
import psycopg2
import pytest
import maya

from psycopg2.extras import DictCursor
from config import settings


@pytest.fixture()
def connection():
    dsl = {
        'dbname': settings.db_name,
        'user': settings.db_user,
        'password': settings.db_password,
        'host': settings.host,
        'port': settings.port
    }
    with sqlite3.connect(settings.db_path) as sqlite_conn, \
            psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        return sqlite_conn.cursor(), pg_conn.cursor()


def test_table_exist_pg(connection):
    sql_curs, pg_curs = connection

    sql_query = r"""SELECT name FROM sqlite_master WHERE type='table';"""
    sql_curs.execute(sql_query)
    sql_tables = [value[0] for value in sql_curs.fetchall()]

    pg_query = r"""
                SELECT tablename
                FROM pg_tables WHERE schemaname='content';
                """
    pg_curs.execute(pg_query)
    for table in pg_curs.fetchall():
        assert table[0] in sql_tables, f'В PG нет таблицы {table[0]}'


def test_count_record(connection):
    sql_curs, pg_curs = connection
    tables = ('film_work', 'person', 'genre',
              'genre_film_work', 'person_film_work')
    for table_name in tables:
        sql_query = f"""SELECT count(*) FROM {table_name};"""
        sql_curs.execute(sql_query)
        count_sql_table = sql_curs.fetchone()
        pg_query = f"""SELECT count(*) FROM content.{table_name};"""
        pg_curs.execute(pg_query)
        count_pg_table = pg_curs.fetchone()
        assert count_sql_table[0] == count_pg_table[0], \
            f'Количество записей для {table_name} не совпадает'


def test_rows_filmworks(connection):
    sql_curs, pg_curs = connection
    sql_query = r"""
        SELECT id, title, description, creation_date,
                rating, type, file_path, created_at, updated_at
        FROM film_work;"""
    sql_curs.execute(sql_query)
    sql_table = sql_curs.fetchall()

    pg_query = r"""
        SELECT id, title, description, creation_date,
                rating, type, file_path, created, modified
        FROM content.film_work;"""
    pg_curs.execute(pg_query)

    pg_table = pg_curs.fetchall()
    for i in range(len(sql_table)):
        for idx in range(9):
            if idx in (7, 8):
                assert maya.parse(sql_table[i][idx]).datetime() == pg_table[i][idx], \
                    f"""Не совпадают поля {sql_table[i][idx]}
                    и {pg_table[i][idx]}"""
                continue
            assert sql_table[i][idx] == pg_table[i][idx], \
                f"""Не совпадают поля {sql_table[i][idx]}
                и {pg_table[i][idx]}"""


def test_rows_person(connection):
    sql_curs, pg_curs = connection
    sql_query = r"""
        SELECT id, full_name, created_at, updated_at
        FROM person;
        """
    sql_curs.execute(sql_query)
    sql_table = sql_curs.fetchall()

    pg_query = r"""
        SELECT id, full_name, created, modified
        FROM content.person;"""
    pg_curs.execute(pg_query)

    pg_table = pg_curs.fetchall()
    for i in range(len(sql_table)):
        for idx in range(4):
            if idx in (2, 3):
                assert maya.parse(sql_table[i][idx]).datetime() == pg_table[i][idx], \
                    f"""Не совпадают поля {sql_table[i][idx]}
                    и {pg_table[i][idx]}"""
                continue
            assert sql_table[i][idx] == pg_table[i][idx], \
                f"""Не совпадают поля {sql_table[i][idx]}
                и {pg_table[i][idx]}"""


def test_rows_genre(connection):
    sql_curs, pg_curs = connection
    sql_query = r"""
        SELECT id, name, description, created_at, updated_at
        FROM genre;
        """
    sql_curs.execute(sql_query)
    sql_table = sql_curs.fetchall()

    pg_query = r"""
        SELECT id, name, description, created, modified
        FROM content.genre;"""
    pg_curs.execute(pg_query)

    pg_table = pg_curs.fetchall()
    for i in range(len(sql_table)):
        for idx in range(5):
            if idx in (3, 4):
                assert maya.parse(sql_table[i][idx]).datetime() == pg_table[i][idx], \
                    f"""Не совпадают поля {sql_table[i][idx]}
                    и {pg_table[i][idx]}"""
                continue
            assert sql_table[i][idx] == pg_table[i][idx], \
                f"""Не совпадают поля {sql_table[i][idx]}
                    и {pg_table[i][idx]}"""


def test_rows_genre_film_work(connection):
    sql_curs, pg_curs = connection
    sql_query = r"""
        SELECT id, film_work_id, genre_id, created_at
        FROM genre_film_work;
        """
    sql_curs.execute(sql_query)
    sql_table = sql_curs.fetchall()

    pg_query = r"""
        SELECT id, film_work_id, genre_id, created
        FROM content.genre_film_work;"""
    pg_curs.execute(pg_query)

    pg_table = pg_curs.fetchall()
    for i in range(len(sql_table)):
        for idx in range(4):
            if idx == 3:
                assert maya.parse(sql_table[i][idx]).datetime() == pg_table[i][idx], \
                    f"""Не совпадают поля {sql_table[i][idx]}
                    и {pg_table[i][idx]}"""
                continue
            assert sql_table[i][idx] == pg_table[i][idx], \
                f"""Не совпадают поля {sql_table[i][idx]}
                и {pg_table[i][idx]}"""


def test_rows_person_film_work(connection):
    sql_curs, pg_curs = connection
    sql_query = r"""
        SELECT id, film_work_id, person_id, role, created_at
        FROM person_film_work;
        """
    sql_curs.execute(sql_query)
    sql_table = sql_curs.fetchall()

    pg_query = r"""
        SELECT id, film_work_id, person_id, role, created
        FROM content.person_film_work;"""
    pg_curs.execute(pg_query)

    pg_table = pg_curs.fetchall()
    for i in range(len(sql_table)):
        for idx in range(5):
            if idx == 4:
                assert maya.parse(sql_table[i][idx]).datetime() == pg_table[i][idx], \
                    f"""Не совпадают поля {sql_table[i][idx]}
                        и {pg_table[i][idx]}"""
                continue
            assert sql_table[i][idx] == pg_table[i][idx], \
                f"""Не совпадают поля {sql_table[i][idx]}
                    и {pg_table[i][idx]}"""
