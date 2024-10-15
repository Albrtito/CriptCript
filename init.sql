CREATE DATABASE IF NOT EXISTS backend_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE backend_db;

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    user_password VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS challenges(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_challenge VARCHAR(255) NOT NULL UNIQUE,
    user VARCHAR(255) NOT NULL,
    content VARCHAR(255) NOT NULL,
    isPrivate TINYINT(1) NOT NULL,
    shared_user VARCHAR(255),
    FOREIGN KEY (user) REFERENCES users(username),
    FOREIGN KEY (shared_user) REFERENCES users(username)
);


INSERT INTO users VALUES('admin', '1234');