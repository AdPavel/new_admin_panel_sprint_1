create table if not exists content.film_work
(
	id uuid not null
		constraint film_work_pkey
			primary key,
	title text not null,
	description text,
	creation_date date,
	rating double precision default 0,
	type text not null,
	created timestamp with time zone default now(),
	modified timestamp with time zone default now(),
	file_path varchar(100),
	certificate text
);

alter table content.film_work owner to app;

create index if not exists film_work_creation_date_rating_idx
	on content.film_work (creation_date, rating);

create index if not exists film_work_type_creation_date_idx
	on content.film_work (type, creation_date);

create table if not exists content.genre
(
	id uuid not null
		constraint genre_pkey
			primary key,
	name varchar(30) not null,
	description text,
	created timestamp with time zone default now(),
	modified timestamp with time zone default now()
);

alter table content.genre owner to app;

create table if not exists content.person
(
	id uuid not null
		constraint person_pkey
			primary key,
	full_name varchar(50) not null,
	created timestamp with time zone default now(),
	modified timestamp with time zone default now()
);

alter table content.person owner to app;

create table if not exists content.genre_film_work
(
	id uuid not null
		constraint genre_film_work_pkey
			primary key,
	genre_id uuid not null
		constraint genre_film_work_genre_id_fkey
			references content.genre
				on delete cascade,
	film_work_id uuid not null
		constraint genre_film_work_film_work_id_fkey
			references content.film_work
				on delete cascade,
	created timestamp with time zone default now()
);

alter table content.genre_film_work owner to app;

create index if not exists genre_film_work_film_work_id_genre_id_idx
	on content.genre_film_work (film_work_id, genre_id);

create table if not exists content.person_film_work
(
	id uuid not null
		constraint person_film_work_pkey
			primary key,
	person_id uuid not null
		constraint person_film_work_person_id_fkey
			references content.person
				on delete cascade,
	film_work_id uuid not null
		constraint person_film_work_film_work_id_fkey
			references content.film_work
				on delete cascade,
	role varchar(50) not null,
	created timestamp with time zone default now()
);

alter table content.person_film_work owner to app;

create unique index if not exists film_work_person_idx
	on content.person_film_work (film_work_id, person_id, role);
