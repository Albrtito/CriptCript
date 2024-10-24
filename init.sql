CREATE DATABASE IF NOT EXISTS backend_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE backend_db;

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    user_password VARCHAR(255)
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

-- insertamos (admin, 1234)
INSERT INTO users VALUES('8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');
