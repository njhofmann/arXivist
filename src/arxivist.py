import utility as u
import search_mode as se
import view_mode as ve
import suggest_mode as sm
import sys


class UserOptions(u.EqualEnum):
    SEARCH = 'search'
    SUGGEST = 'suggest'
    VIEW = 'view'
    EXIT = 'exit'


def parse_mode(mode: str) -> None:
    if mode == UserOptions.VIEW:
        ve.view_mode()
    elif mode == UserOptions.SEARCH:
        se.search_mode()
    elif mode == UserOptions.SUGGEST:
        sm.suggest_mode()
    elif mode == UserOptions.EXIT:
        sys.exit()
    else:
        raise ValueError(f'{mode} is not a supported mode')


def main():
    while True:
        try:
            user_mode = input(f"available modes are {', '.join([mode.value for mode in UserOptions])}\n")
            parse_mode(user_mode)
        except Exception as e:
            raise e


if __name__ == '__main__':
    main()
