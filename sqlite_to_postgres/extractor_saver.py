import uuid
from dataclasses import dataclass


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
    rating: float
    type: str
    created_at: str
    updated_at: str


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


def sql_to_pg(curs, table_name, data):
    column_name = get_column_name(curs, table_name)
    fields_name = ', '.join(column_name)
    for field in column_name:
        data[table_name][field]

    args = []

    curs.execute(f"""
        INSERT INTO content.{table_name} ({fields_name})
        VALUES {args}
    """)


def from_dictrow_to_list(fetchall):
    # Функция преоброзования DictRow в список строк.
    return [value[0] for value in fetchall]


def to_genre(curs, genre: Genre):
    pass


def to_genre_film_work(curs, genre_film_work: GenreFilmWork):
    pass


def to_person_film_work(curs, person_film_work: PersonFilmWork):
    pass


def to_person(curs, person: Person):
    pass

# закончил здесь, потом можно будет в функцию перенести только сбор скульного запроса
def to_film_work(curs, filmwork: FilmWork):
    s = 0; chunk = n = int(len(filmwork) * 0.1) + 1
    while filmwork[s:chunk]:
        for row in filmwork[s:chunk]:
            print() # тут можно собирать аргумент по количеству в чанке и отправлять в другую функцию для загрузкив БД
        #     блин хрен там поля у разных таблиц разные, хотя можно аргументы из строк парсить, что то типа
        #  [filmwork.id, filmwork.title и т.д.] а потом отправлять в sql_to_pg
        s, chunk = chunk, chunk + n
        print(s, chunk)


class PostgresSaver:
    func_dict = {
        'Genre': to_genre,
        'genre_film_work': to_genre_film_work,
        'person_film_work': to_person_film_work,
        'person': to_person,
        'film_work': to_film_work
    }

    def __init__(self, pg_conn):
        self.pg_conn = pg_conn

    def save_all_data(self, data):
        curs = self.pg_conn.cursor()
        tables = get_tables(curs)
        # clear_base(curs, tables)
        for table_name in tables:
            self.func_dict[table_name](curs, data[table_name])
            # sql_to_pg(curs, table_name, data)


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
