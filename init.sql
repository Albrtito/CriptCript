GRANT ALL PRIVILEGES ON *.* TO 'admin@localhost.com'@'%' IDENTIFIED BY '1234' WITH GRANT OPTION;

CREATE DATABASE IF NOT EXISTS backend_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE backend_db;

CREATE TABLE IF NOT EXISTS users (
    username VARCHAR(255) NOT NULL UNIQUE PRIMARY KEY,
    user_password VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS public_challenges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_challenge BLOB NOT NULL UNIQUE,
    user VARCHAR(255) NOT NULL,
    content BLOB NOT NULL,
    auth BLOB,
    FOREIGN KEY (user) REFERENCES users(username)
);

CREATE TABLE IF NOT EXISTS private_challenges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name_challenge BLOB NOT NULL UNIQUE,
    user VARCHAR(255) NOT NULL,
    content BLOB NOT NULL,
    auth BLOB,
    shared_user VARCHAR(255),
    FOREIGN KEY (user) REFERENCES users(username),
    FOREIGN KEY (shared_user) REFERENCES users(username)
);

-- insertamos (admin, 1234) 
--INSERT INTO users VALUES('8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', --'03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');

CREATE DATABASE IF NOT EXISTS digital_firm
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_general_ci;

USE digital_firm;

CREATE TABLE IF NOT EXISTS secure_keys(
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    encrypted_private_key BLOB, -- AES256, ciframos esta clave igual que los mensajes (con la contraseña del user)
    public_key VARCHAR(512) -- public, no nos importa cifrarla (por eso es string). Pero RSA-2048, necesitamos 512
);

CREATE TABLE IF NOT EXISTS digital_signatures(
    id INT AUTO_INCREMENT PRIMARY KEY, 
    content BLOB NOT NULL,
    signature BLOB NOT NULL -- firma del mensaje. Cuando recuperemos el mensaje, vendremos a esta base de datos y sacaremos la firma para luego trabajar con ella
);
