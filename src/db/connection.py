import pg8000.native
from src.db.config import user, password, host, port, database


def connect_to_db():
    return pg8000.native.Connection(
        user,
        password=password,
        host=host,
        port=port,
        database=database,
    )


def close_db_connection(conn):
    conn.close()
