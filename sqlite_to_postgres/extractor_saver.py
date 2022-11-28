import uuid
import datetime
from random import randrange
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Genre:
    id: str
    name: str
    description: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class GenreFilmWork:
    id: str
    film_work_id: str
    genre_id: str
    created_at: str


@dataclass(frozen=True)
class PersonFilmWork:
    id: str
    film_work_id: str
    person_id: str
    role: str
    created_at: str


@dataclass(frozen=True)
class Person:
    id: str
    full_name: str
    created_at: str
    updated_at: str


@dataclass(frozen=True)
class FilmWork:
    id: str
    title: str
    description: str
    creation_date: str
    file_path: str
    type: str
    created_at: str
    updated_at: str
    rating: float = field(default=0.0)


def clear_base(curs, tables):
    # Очистка данных из таблиц БД.
    for table_name in tables:
        curs.execute(f"""TRUNCATE content.{table_name} CASCADE""")


def get_tables(curs):
    # Получить список названий таблиц.
    curs.execute(r"""SELECT tablename FROM pg_tables WHERE schemaname='content';""")
    tables = from_dictrow_to_list(curs.fetchall())
    return tables


def get_column_name(curs, table_name):
    # Получить списко наименование полей.
    curs.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{table_name}' AND table_schema = 'content';
    """)
    column_name = from_dictrow_to_list(curs.fetchall()) #[value[0] for value in curs.fetchall()]
    return column_name


# def sql_to_pg(curs, table_name, data):
#     column_name = get_column_name(curs, table_name)
#     fields_name = ', '.join(column_name)
#     for field in column_name:
#         data[table_name][field]
#
#     args = []
#
#     curs.execute(f"""
#         INSERT INTO content.{table_name} ({fields_name})
#         VALUES {args}
#     """)


def from_dictrow_to_list(fetchall):
    # Функция преоброзования DictRow в список строк.
    return [value[0] for value in fetchall]

# def make_execute(pg_conn, table, data, sql_query):
#     curs = pg_conn.cursor()
#     s = 0
#     chunk = n = int(len(table) * 0.1) + 1
#
#     while table[s:chunk]:
#         for row in table[s:chunk]:
#             data.append(data)
#         curs.executemany(sql_query, data)
#         pg_conn.commit()
#         s, chunk = chunk, chunk + n


def save_to_genre(table_chunk):
    sql_query = """
        INSERT INTO content.genre(id, name, description, created, modified)
        VALUES (%s, %s, %s, %s, %s)  
        """
    data = [(row.id, row.name, row.description, row.created_at, row.updated_at) for row in table_chunk]

    return sql_query, data


def save_to_genre_film_work(table_chunk):
    sql_query = """
        INSERT INTO content.genre_film_work(id, genre_id, film_work_id, created)
        VALUES (%s, %s, %s, %s)  
        """
    data = [(row.id, row.genre_id, row.film_work_id, row.created_at) for row in table_chunk]

    return sql_query, data


def save_to_person_film_work(table_chunk):
    sql_query = """
        INSERT INTO content.person_film_work(id, person_id, film_work_id, role, created)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT do nothing 
        """
    data = [(row.id, row.person_id, row.film_work_id, row.role, row.created_at) for row in table_chunk]

    return sql_query, data


def save_to_person(table_chunk):
    sql_query = """
        INSERT INTO content.person(id, full_name, created, modified)
        VALUES (%s, %s, %s, %s) ON CONFLICT do nothing 
        """

    data = [(row.id, row.full_name, row.created_at, row.updated_at) for row in table_chunk]

    return sql_query, data


def save_to_film_work(table_chunk):
    # curs = pg_conn.cursor()

    sql_query = """
        INSERT INTO content.film_work (id, title, description, creation_date, rating,
         type, created, modified, file_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT do nothing 
        """
    # data = (filmwork.id, filmwork.title, filmwork.description,
    #         datetime.date(randrange(2000, 2020), randrange(1, 12), randrange(1, 28)),
    #         filmwork.rating, filmwork.type, filmwork.created_at, filmwork.updated_at, filmwork.file_path)
    #
    # make_execute(pg_conn, filmwork, data, sql_query)

    # while filmwork[start:chunk]:
    data = [(row.id, row.title, row.description,
             datetime.date(randrange(2000, 2020), randrange(1, 12), randrange(1, 28)),
             row.rating, row.type, row.created_at, row.updated_at, row.file_path)
            for row in table_chunk]

    # for row in table_chunk:
    #     data.append((row.id, row.title, row.description,
    #                  datetime.date(randrange(2000, 2020), randrange(1, 12), randrange(1, 28)),
    #                  row.rating, row.type, row.created_at, row.updated_at, row.file_path))

    return sql_query, data

        # curs.executemany(sql_query, data)
        # pg_conn.commit()
        # start, chunk = chunk, chunk + n


class PostgresSaver:
    func_dict = {
        'genre': save_to_genre,
        'genre_film_work': save_to_genre_film_work,
        'person_film_work': save_to_person_film_work,
        'person': save_to_person,
        'film_work': save_to_film_work
    }

    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, data):
        curs = self.pg_conn.cursor()
        tables = ('film_work', 'person', 'genre', 'genre_film_work', 'person_film_work')#get_tables(curs)
        # clear_base(curs, tables)
        for table_name in tables:
            start = 0
            chunk = n = int(len(data[table_name]) * 0.1) + 1
            # self.func_dict[table_name](self.pg_conn, curs, data[table_name], 0, chunk, n)

            while table_chunk := data[table_name][start:chunk]:
                sql_query, chunk_data = self.func_dict[table_name](table_chunk)
                curs.executemany(sql_query, chunk_data)
                self.pg_conn.commit()
                start, chunk = chunk, chunk + n

        # chunk = n = int(len(data['person_film_work']) * 0.1) + 1
        # self.func_dict['person_film_work'](self.pg_conn, curs, data['person_film_work'], 0, chunk, n)


class SQLiteExtractor:
    def __init__(self, conn):
        self.conn = conn

    def extract_movies(self):
        dataclass_dict = {'genre': Genre,
                          'genre_film_work': GenreFilmWork,
                          'person_film_work': PersonFilmWork,
                          'person': Person,
                          'film_work': FilmWork}
        data = dict()
        curs = self.conn.cursor()
        for key in dataclass_dict:
            curs.execute(f"""SELECT * FROM {key};""")
            data[key] = [dataclass_dict[key](**row) for row in curs.fetchall()]
        return data
