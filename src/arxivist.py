from __future__ import annotations
from typing import List
import pathlib as pl
import sys
import read_env as re
import src.modes.search_mode as se
import src.modes.view_modes as ve
import src.modes.suggest_mode as sm
import src.utility.save_query as sq
import src.utility.cmd_enum as ce
import src.db_init as db
import src.util as u

"""Main entry point for the arXives shell. Displays set of supported "modes" (search, viewing, suggestion, etc.) user
can select from."""


def load_env_file(env_path: pl.Path) -> None:
    if not pl.Path(env_path).exists():
        raise RuntimeError(f'path to config file {env_path} doesn\'t exist')
    re.read_env(env_path, recurse=False)


ENV_FILE = pl.Path(__file__).parent.parent.joinpath('.env')
SCHEMA_FILE = pl.Path(__file__).parent.parent.joinpath('init.sql')


class UserOptions(ce.CmdEnum):
    """Set of supported "modes" mapped to allocated keywords for calling."""
    SEARCH = ce.Command('search', lambda x: se.search_mode(), 'search for papers')
    SUGGEST = ce.Command('suggest', lambda x: sm.suggest_mode(), 'suggested papers based on gathered citations')
    SAVED = ce.Command('saved', lambda x: ve.view_mode(), 'view previously saved papers')
    EXIT = ce.Command('exit', lambda x: sys.exit(), 'exit the program')
    HELP = ce.Command('help', lambda x: UserOptions.display_help_options(), 'what each mode does')

    @classmethod
    def execute_params(cls, params: List[str], search_query: sq.SaveQuery = None) -> UserOptions:
        return super().execute_params(params, search_query)
        if not params or len(params) > 1:
            raise ValueError(f'only require command name to select a mode')


def main(sys_mode: str) -> None:
    if sys_mode not in ('prod', 'dev'):
        raise ValueError(f'{sys_mode} is an unsupported system mode')

    # load env variables, init_db
    load_env_file(ENV_FILE)
    db.init_db(SCHEMA_FILE)

    while True:
        try:
            UserOptions.display_available_options()
            user_mode = u.get_user_input('').split(' ')
            UserOptions.execute_params(user_mode)
        except Exception as e:
            if sys_mode != 'prod':
                raise e
            print(e)


if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) != 1:
        raise ValueError('require only one argument to select mode shell runs in')
    main(args[0])
