import psycopg2 as psy
import pathlib as pl
from typing import Union
import dataclasses as dc
import read_env as re
import os


@dc.dataclass(frozen=True)
class DatabaseConfig:
    """Stores name of a database and database info (username and password)"""
    db_name: str  # database name
    user: str  # name to login to database system with
    password: str  # password to login into the database system with


def get_db_info(config_file: Union[str, pl.Path]) -> DatabaseConfig:
    """
    Opens the database configuration file at the given path and returns database name and login info stored inside.
    :param config_file: path to config file
    :return: DatabaseConfig with read in file
    """
    # check file exists
    if not pl.Path(config_file).exists():
        raise RuntimeError(f'path to config file {config_file} doesn\'t exist')

    # read in config info
    re.read_env(config_file)
    return DatabaseConfig(os.environ['POSTGRES_DB'], os.environ['POSTGRES_USER'], os.environ['POSTGRES_PASSWORD'])


def init_db(config_file: Union[str, pl.Path], schema_file: Union[str, pl.Path]) -> None:
    """Creates a new database for arXives using configuration info stored in given file path, then reads in the needed
    schema stored in the given schema path.
    :param config_file: path to config file
    :param schema_file: path to schema file
    :return: None
    """
    conn_info = get_db_info(config_file)
    with psy.connect(user=conn_info.user, password=conn_info.user) as conn:
        with conn.cursor() as cursor:
            # check that database with same name doesn't exist
            cursor.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
            databases = set([database[0] for database in cursor.fetchall()])
            if conn_info.db_name in databases:
                raise RuntimeError(f'database with name {conn_info.db_name} already exists')

            # create new database
            cursor.execute(f'CREATE DATABASE {conn_info.db_name}')

            # read in schema file
            cursor.execute(open(schema_file).read())


if __name__ == '__main__':
    init_db('db.env', 'init.sql')
