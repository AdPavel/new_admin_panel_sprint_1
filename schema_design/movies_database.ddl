CREATE SCHEMA IF NOT EXISTS content;


CREATE TABLE IF NOT EXISTS content.film_work (
    id uuid PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    rating FLOAT,
    type TEXT not null,
    created timestamp with time zone,
    modified timestamp with time zone
);

CREATE TABLE IF NOT EXISTS content.genre (
    id uuid PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description TEXT,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person (
    id uuid PRIMARY KEY,
    full_name VARCHAR(30) NOT NULL,
    created TIMESTAMP WITH TIME ZONE,
    modified TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id uuid PRIMARY KEY,
    genre_id uuid,
    film_work_id uuid,
    FOREIGN KEY (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    created TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS content.person_film_work (
    id uuid PRIMARY KEY,
    person_id uuid,
    film_work_id uuid,
    FOREIGN KEY (person_id) REFERENCES content.person (id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    role VARCHAR(30),
    created TIMESTAMP WITH TIME ZONE
);

-- Создание индексов

CREATE INDEX film_work_creation_date_rating_idx ON content.film_work(creation_date, rating);
CREATE INDEX film_work_type_creation_date_idx ON content.film_work(type, creation_date);

CREATE UNIQUE INDEX film_work_person_idx ON content.person_film_work (film_work_id, person_id);
CREATE INDEX ON content.genre_film_work (film_work_id, genre_id);
