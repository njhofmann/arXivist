from __future__ import annotations
from typing import List
import utility as u
import search_mode as se
import view_mode as ve
import suggest_mode as sm
import sys


class UserOptions(u.CommandEnum):
    SEARCH = 'search'
    SUGGEST = 'suggest'
    VIEW = 'view'
    EXIT = 'exit'

    @classmethod
    def execute_params(cls, params: List[str], search_query: u.SaveQuery = None) -> UserOptions:
        if not params or len(params) > 1:
            raise ValueError(f'UserOptions only requires one param')

        mode = params[0]
        if mode == UserOptions.VIEW:
            ve.view_mode()
            return UserOptions.VIEW
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


def main():
    while True:
        try:
            user_mode = input(f"available modes are {UserOptions.values_as_str()}\n").split(' ')
            UserOptions.execute_params(user_mode)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
