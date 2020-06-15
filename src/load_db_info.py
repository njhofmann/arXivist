import pathlib as pl
import os
import database.db_init as dc


"""Module for managing database configuration info for source files by adding and retrieving them to the system's 
environment variables."""

# data info labels
DB_NAME = 'db_name'
USERNAME = 'username'
PASSWORD = 'password'


def load_db_info(config_path: pl.Path) -> None:
    database_config = dc.get_db_info(config_path)
    environ_to_config = [(DB_NAME, database_config.db_name), (USERNAME, database_config.user),
                         (PASSWORD, database_config.password)]
    for env, config in environ_to_config:
        os.environ[env] = config


def get_db_name():
    if DB_NAME not in os.environ:
        raise ValueError('database name not added to environment variables')
    return os.environ[DB_NAME]


def get_username():
    if USERNAME not in os.environ:
        raise ValueError('username not added to environment variables')
    return os.environ[USERNAME]


def get_password():
    if PASSWORD not in os.environ:
        raise ValueError('password name not added to environment variables')
    return os.environ[PASSWORD]
