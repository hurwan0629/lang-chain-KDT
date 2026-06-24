CREATE DATABASE temp_movie;

USE temp_movie; 

DROP TABLE movies;

CREATE TABLE movies(
	movie_pk BIGINT AUTO_INCREMENT PRIMARY KEY,
	movie_title VARCHAR(50) DEFAULT '제목없음',
	movie_subtitle VARCHAR(100),
	movie_genre_pk BIGINT NOT NULL,
	movie_release_at TIMESTAMP NOT NULL DEFAULT NOW(),
	movie_deleted TINYINT NOT NULL DEFAULT 0
);

ALTER TABLE movies
ADD CONSTRAINT movie_genre_fk
FOREIGN KEY (movie_genre_pk) REFERENCES genres (genre_pk);



CREATE TABLE genres(
	genre_pk BIGINT AUTO_INCREMENT PRIMARY KEY,
	genre_name VARCHAR(50) NOT NULL UNIQUE,
	genre_created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	genre_can_used TINYINT NOT NULL DEFAULT 1
);

