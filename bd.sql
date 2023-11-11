DROP DATABASE IF EXISTS SRP;

CREATE DATABASE SRP;
USE SRP;

CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    names VARCHAR(20),
    lastnames VARCHAR(20),
    email VARCHAR(40),
    password VARCHAR(20)
);

CREATE TABLE rating (
    id INT AUTO_INCREMENT PRIMARY KEY,
    movieId INT,
    userId INT,
    rating DECIMAL(2,1),
    FOREIGN KEY (userId) REFERENCES user(id)
);

CREATE TABLE movie (
	id INT PRIMARY KEY,
    title VARCHAR(100),
    year INT
);

CREATE TABLE link (
	id INT AUTO_INCREMENT PRIMARY KEY,
    movieId INT,
    imdbId INT,
    tmdbId INT,
    FOREIGN KEY (movieId) REFERENCES movie(id)
);

DROP PROCEDURE IF EXISTS sp_verifyIdentity;

DELIMITER $$

CREATE PROCEDURE `sp_verifyIdentity` (
    IN `pEmail` VARCHAR(40),
    IN `pPassword` VARCHAR(20)
)  
BEGIN
    SELECT id, names, lastnames, email, password
    FROM user
    WHERE email = pEmail 
    AND password = pPassword;
END$$

DELIMITER ;


SELECT id, names, lastnames, email, password FROM user ORDER BY names ASC;
SELECT id, movieId, userId, rating FROM rating ORDER BY movieId ASC;
SELECT id, title, year FROM movie ORDER BY id ASC;
SELECT id, movieId, imdbId, tmdbId FROM link;

SELECT movieId, rating FROM rating WHERE userId = 1;