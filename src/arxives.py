from __future__ import annotations
from typing import List
from modes import search_mode as se, save_mode as ve, suggest_mode as sm
import src.utility.save_query as sq
import src.utility.command_enum as ce
import database.db_init as dc
import os
import pathlib as pl
import sys

"""Main entry point for the arXives shell. Displays set of supported "modes" (search, viewing, suggestion, etc.) user
can select from."""


CONFIG_PATH = pl.Path('.').parent.parent.joinpath('database').joinpath('config.yaml').resolve()

class UserOptions(ce.CommandEnum):
    """Set of supported "modes" mapped to allocated keywords for calling."""
    SEARCH = 'search'  # search for papers
    SUGGEST = 'suggest'  # suggest papers based on gathered citations
    SAVED = 'saved'  # view previously saved papers
    EXIT = 'exit'  # exit the shell

    @classmethod
    def execute_params(cls, params: List[str], search_query: sq.SaveQuery = None) -> UserOptions:
        if not params or len(params) > 1:
            raise ValueError(f'only require command name to select a mode')

        mode = params[0]
        if mode == UserOptions.SAVED:
            ve.save_mode()
            return UserOptions.SAVED
        elif mode == UserOptions.SEARCH:
            se.search_mode()
            return UserOptions.SEARCH
        elif mode == UserOptions.SUGGEST:
            sm.suggest_mode()
            return UserOptions.SUGGEST
        elif mode == UserOptions.EXIT:
            sys.exit()
        else:
            raise ValueError(f'{mode} is not a supported mode')


def load_db_info(config_path: pl.Path) -> None:
    database_config = dc.open_config(config_path)
    os.environ['db_name']


def main(sys_mode: str) -> None:
    if sys_mode not in ('prod', 'dev'):
        raise ValueError(f'{sys_mode} is an unsupported system mode')

    # initalize db variables
    load_db_info(CONFIG_PATH)

    while True:
        try:
            user_mode = input(f"available modes are {UserOptions.values_as_str()}\n").split(' ')
            UserOptions.execute_params(user_mode)
        except Exception as e:  # print if prod else raise error
            if sys_mode == 'prod':
                print(e)
            else:
                raise e


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        raise ValueError('require only one argument to select mode shell runs in')
    main(args[0])
