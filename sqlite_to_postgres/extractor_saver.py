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
    file_path: str
    type: str
    created_at: str
    updated_at: str
    creation_date: str = field(default='null')
    rating: float = field(default=0.0)


def save_to_genre(table_chunk):
    sql_query = """
        INSERT INTO content.genre(id, name, description, created, modified)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
        """
    data = [(row.id, row.name, row.description, row.created_at, row.updated_at)
            for row in table_chunk]
    return sql_query, data


def save_to_genre_film_work(table_chunk):
    sql_query = """
        INSERT INTO content.genre_film_work(id, genre_id,
                                            film_work_id, created)
        VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
        """
    data = [(row.id, row.genre_id, row.film_work_id, row.created_at)
            for row in table_chunk]
    return sql_query, data


def save_to_person_film_work(table_chunk):
    sql_query = """
        INSERT INTO content.person_film_work(id, person_id, film_work_id,
                                            role, created)
        VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
        """
    data = [(row.id, row.person_id, row.film_work_id, row.role, row.created_at)
            for row in table_chunk]
    return sql_query, data


def save_to_person(table_chunk):
    sql_query = """
        INSERT INTO content.person(id, full_name, created, modified)
        VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING
        """
    data = [(row.id, row.full_name, row.created_at, row.updated_at)
            for row in table_chunk]
    return sql_query, data


def save_to_film_work(table_chunk):
    sql_query = """
        INSERT INTO content.film_work (id, title, description, creation_date,
         rating, type, created, modified, file_path)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING
        """
    data = [(row.id, row.title, row.description,
             row.creation_date, row.rating, row.type,
             row.created_at, row.updated_at, row.file_path)
            for row in table_chunk]
    return sql_query, data


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
        tables = ('film_work', 'person', 'genre',
                  'genre_film_work', 'person_film_work')
        for table_name in tables:
            start = 0
            chunk = n = int(len(data[table_name]) * 0.1) + 1
            while table_chunk := data[table_name][start:chunk]:
                sql_query, chunk_data = self.func_dict[table_name](table_chunk)
                curs.executemany(sql_query, chunk_data)
                self.pg_conn.commit()
                start, chunk = chunk, chunk + n


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
