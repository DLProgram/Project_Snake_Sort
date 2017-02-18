import pymysql
import getpass
from database import create_tables

DB_NAME = "snake_sort"


def connect_to_server():
    """Connect to the MySQL server based on user input.

    Returns:
        pymysql.connection object to the server.

    """
    return pymysql.connect(host="localhost",
                           user=input("Username: ").strip(),
                           password=getpass.getpass())


def choose_db(conn, db_name: str) -> str:
    """Select the db and create it if it doesn't exist.

    Args:
        conn: pymysql.connection object to the MySQL server.
        db_name: name of the database.

    Returns:
        A status string.

    """
    with conn.cursor() as cursor:
        if cursor.execute("SHOW DATABASES LIKE '{}';".format(db_name)):
            cursor.execute("USE {};".format(db_name))
            return "Database {} exsit!".format(db_name)
        else:
            cursor.execute("CREATE DATABASE IF NOT EXISTS {};".format(db_name))
            cursor.execute("USE {};".format(db_name))
            return "Database {} created!".format(db_name)


def check_table(conn, table: str) -> str:
    """Check if the table exist, create it if it doesn't

    Args:
        conn: pymysql.connection object to the MySQL server.
        table: name of the table.

    Returns:
        A status string.

    """
    with conn.cursor() as cursor:
        return bool(cursor.execute("SHOW TABLES LIKE '{}';".format(table)))


def create_user(conn, db_name: str):
    """Create a database specific user named 'snake'

    Args:
        conn: pymysql.connection object to the MySQL server.
        db_name: name of the database.

    """
    command = """
    CREATE USER 'snake'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON `{}`.* TO 'snake'@'localhost';"""
    with conn.cursor() as cursor:
        cursor.execute(command.format(db_name))


def main():
    conn = connect_to_server()
    print("Connected to server!")
    print(choose_db(conn, DB_NAME))
    print(create_user(conn, DB_NAME))
    create_tables()

if __name__ == '__main__':
    main()
