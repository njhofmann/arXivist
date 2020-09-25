import abc
import argparse as ap
from typing import Iterable, List
import src.util as u


class ArgumentParserException(Exception):
    """An Exception for an when error occurs in an ArgumentParser"""
    pass


class RaisingArgParser(ap.ArgumentParser):
    """Custom ArgumentParser class that raises exceptions instead of exiting the system."""

    def error(self, msg: str):
        raise ArgumentParserException(msg)


class BaseQuery(abc.ABC):

    def __init__(self, title_args: Iterable[str] = (), author_args: Iterable[str] = (),
                 abstract_args: Iterable[str] = (), id_args: Iterable[str] = (),
                 max_result: int = 10, start: int = 0) -> None:
        self.title_args = title_args
        self.author_args = author_args
        self.abstract_args = abstract_args
        self.id_args = id_args
        self.max_result = max_result
        self.start = start

    @classmethod
    def get_parser(cls) -> RaisingArgParser:
        """Returns an RaisingArgParser for creating a BaseQuery
        :return: custom ArgumentParser
        """
        parser = RaisingArgParser(prefix_chars='-', description='parse paper search arguments')
        parser.add_argument('-a', '--all', nargs='*', type=str, default=[], help='apply argument to every other arg')
        parser.add_argument('-id', '--arvix_id', nargs='*', type=str, default=[], help='search by arxiv id')
        parser.add_argument('-t', '--title', nargs='*', type=str, default=[], help='search by words in title')
        parser.add_argument('-au', '--author', nargs='*', type=str, default=[], help='search by parts of author name')
        parser.add_argument('-ab', '--abstract', nargs='*', type=str, default=[], help='search by words in abstract')
        return parser

    @classmethod
    def from_args(cls: type):
        """Asks the user for a list of arguments, creating an instance of this BaseQuery (or subclass) from them.
        :param cls: the type of the class being created (BaseQuery of subclass)
        :param args: list of arguments to create the class from
        :return: instantiated class of given type"""
        parser = cls.get_parser()
        while True:
            try:
                args = u.get_formatted_user_input('enter search params')
                args = parser.parse_args(args)
                return cls(title_args=args.title + args.all,
                           id_args=args.arvix_id + args.all,
                           abstract_args=args.abstract + args.all,
                           author_args=args.author + args.all)
            except ArgumentParserException as e:
                print(e)
