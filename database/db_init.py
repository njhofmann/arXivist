import psycopg2 as psy
import yaml as y
import pathlib as pl
from typing import Union
import dataclasses as dc


@dc.dataclass
class DatabaseConfig:
    """Stores name of a database and database info (username and password)."""
    db_name: str  # database name
    user: str  # name to
    password: str


def open_config(config_file: Union[str, pl.Path]) -> DatabaseConfig:
    """
    Opens the database configuration file at the given path and returns database name and login info stored inside.
    :param config_file: path to config file
    :return: DatabaseConfig with read in fo
    """
    # check file exists
    if not pl.Path(config_file).exists():
        raise RuntimeError(f'path to config file {config_file} doesn\'t exist')

    # read in config info
    with open(config_file, 'r') as config:
        yaml_reader = y.parse(config.read(), y.FullLoader)
        return DatabaseConfig(yaml_reader['DATABASE'], yaml_reader['USER'], yaml_reader['PASSWORD'])


def init_db(config_file: Union[str, pl.Path], schema_file: Union[str, pl.Path]) -> None:
    """
    Creates a new database for arXives using configuration info stored in given file path, then reads in the needed
    schema stored in the given schema path.
    :param config_file: path to config file
    :param schema_file: path to schema file
    :return: None
    """
    conn_info = open_config(config_file)
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
    init_db('config.yaml', 'schema.sql')
