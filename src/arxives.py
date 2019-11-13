import utility as u
import search_mode as se
import view_mode as ve
import suggest_mode as sm
import sys


class UserOptions(u.CommandEnum):
    SEARCH = se.search_mode
    SUGGEST = sm.suggest_mode
    VIEW = ve.view_mode
    EXIT = sys.exit


def main():
    while True:
        try:
            user_mode = input(f"available modes are {UserOptions.values_as_str()}\n")
            UserOptions.get_command_method(user_mode)()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main()
