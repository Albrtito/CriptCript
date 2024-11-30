import mysql.connector

DATABASE_NAME = "backend_db"
def get_db_connection():
    connection = mysql.connector.connect(
        host="mariadb",
        user="admin@localhost.com",
        password="1234",
        database=DATABASE_NAME,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    return connection

DATABASE_DIGITAL_SIGN_NAME = "digital_firm"
def get_digital_sign_db_connection():
    connection = mysql.connector.connect(
        host="mariadb",
        user="admin@localhost.com",
        password="1234",
        database=DATABASE_DIGITAL_SIGN_NAME,
        charset='utf8mb4',
        collation='utf8mb4_general_ci'
    )
    return connection  