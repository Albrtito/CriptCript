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
INSERT INTO users VALUES('8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4');

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

INSERT INTO secure_keys (username, encrypted_private_key, public_key)
VALUES (
    '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',
    'MIIEpAIBAAKCAQEA9WLM8AqokZz7SVBmxh881llE7nZjxTrGvgITj/Aqsxg1JmmA3QldQ2myRq1OzIS9jnPDHqwGpLfCVMZ64buH+6ON4u+ss85Fe8TikB6O430OwMopQeP5Glr6UOMFfvntL0Nuprs7DQRlzzBueMgmXdNTGx1cbtqKhREDawWhdJa32GPlD5RhBCmn1YejkmOpMQKvzXJhXMffwCrNRWXcA3m5atT38jbIXkc1X7S0F0LO/DM+tY7OLIGxd/3RYXs88v3L2ESmvhQbWXG74BJz+pNKcGiaAKixUmchH69HPEIl9kIfVX9bdI7CLeVLhxvPSaKAMiJrBaWHy4a9CzUKywIDAQABAoIBABKgf4ZghhTuRy70sPssx4f35SElkIOaEhhop5vUsyZphINYHTrqKTpi+Br1sJZwJG7Uqm+WHGJS5qgGcbEtSfBtT78gdXTSss3nOfw5rZwRfqteIo1Iumc97Q7Iej7TcaXq/FJ2F6XwewVOxlwEdCZ0J7SrtmazJTJeV8A/KwHirElMKwHDfeUfO0h1fD2gPSG0VFpxvwXDFojdY5lufm6d5r7iPBgCQ296bqC9Im7tBz5bGetRHDBOF81nfh30av/7qpH/ySqG+Qs1URabjQqdBwVnSCoAT/ac5HrM3R78Y5GsJqjE6j1qozBqZCUpcVPXkLTBqHdVBL/rSt3Rzu0CgYEA/39Cf10mSjqBR07IRv/xVDTZCo6JTjHVLDYHaPhFYrpheuHxBkq/N9qMgDPEF6KwjfsS+j5BVHTXQqqpcyaMsquNpZ/ZQ9KccvePEbzFRjE3yuL3gcBWypR1ZXVr+KMl+JYQrJ4vgW9VxwcYaMOMspOq9CU8mF6XD1rRGqJurtc',
    'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA9WLM8AqokZz7SVBmxh881llE7nZjxTrGvgITj/Aqsxg1JmmA3QldQ2myRq1OzIS9jnPDHqwGpLfCVMZ64buH+6ON4u+ss85Fe8TikB6O430OwMopQeP5Glr6UOMFfvntL0Nuprs7DQRlzzBueMgmXdNTGx1cbtqKhREDawWhdJa32GPlD5RhBCmn1YejkmOpMQKvzXJhXMffwCrNRWXcA3m5atT38jbIXkc1X7S0F0LO/DM+tY7OLIGxd/3RYXs88v3L2ESmvhQbWXG74BJz+pNKcGiaAKixUmchH69HPEIl9kIfVX9bdI7CLeVLhxvPSaKAMiJrBaWHy4a9CzUKywIDAQAB'
);
