CREATE DATABASE egy_imdb1;
USE egy_imdb1;
CREATE TABLE movie(
movie_name nvarchar(50) NOT NULL,
release_date date NOT NULL,
duration time NOT NULL,
movie_description varchar(2000),
rating varchar(20),
revenue decimal,
CONSTRAINT PK_MOVIE PRIMARY KEY(movie_name, release_date)
);
CREATE TABLE movie_genre(
movie_name nvarchar(50) NOT NULL,
release_date date NOT NULL,
genre varchar(50) NOT NULL,
CONSTRAINT FK_GENRE FOREIGN KEY (movie_name, release_date) REFERENCES movie(movie_name, release_date)
);
ALTER TABLE movie
ALTER COLUMN duration SET default '00:00:00';
ALTER TABLE movie
ALTER COLUMN release_date SET default '2000-01-01';
ALTER TABLE movie_genre
ALTER COLUMN release_date SET default '2000-01-01';
CREATE TABLE cast_member(
member_name nvarchar(255) NOT NULL,
nationality varchar(20) NOT NULL,
birthdate date NOT NULL,
biography varchar(3000),
CONSTRAINT PK_CAST PRIMARY KEY(member_name, birthdate)
);
CREATE TABLE acted_in(
movie_name nvarchar(50) NOT NULL,
member_name nvarchar(255) NOT NULL,
member_role varchar(20) NOT NULL,
FOREIGN KEY (movie_name) REFERENCES movie(movie_name),
FOREIGN KEY (member_name) REFERENCES cast_member(member_name)
);
CREATE TABLE imdb_user(
email varchar(255) PRIMARY KEY NOT NULL,
username varchar(255) NOT NULL,
gender char NOT NULL,
birthdate date NOT NULL
);
CREATE TABLE review(
user_email varchar(255) NOT NULL,
movie_name varchar(255) NOT NULL,
release_date date NOT NULL,
review_text varchar(2000),
rate tinyint PRIMARY KEY NOT NULL,
FOREIGN KEY (user_email) REFERENCES imdb_user(email),
CONSTRAINT FK_REVIEW FOREIGN KEY (movie_name, release_date) REFERENCES movie(movie_name, release_date)
);