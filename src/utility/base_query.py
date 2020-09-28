import abc
import argparse as ap
from typing import Iterable

import src.util as u


class ArgumentParserException(Exception):
    """An Exception for an when error occurs in an ArgumentParser"""
    pass


class RaisingArgumentParser(ap.ArgumentParser):
    """Custom ArgumentParser class that raises exceptions instead of exiting the system."""

    def error(self, msg: str):
        """Raise a ArgumentParserException with the given error message
        :param msg: error message to raise
        :return: None
        """
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
    def get_parser(cls) -> RaisingArgumentParser:
        """Returns an RaisingArgParser for creating a BaseQuery
        :return: custom ArgumentParser
        """
        parser = RaisingArgumentParser(prefix_chars='-', description='parse paper search arguments')
        parser.add_argument('-a', '--all', nargs='*', type=str, default=[], help='apply argument to every other arg')
        parser.add_argument('-id', '--arvix_id', nargs='*', type=str, default=[], help='search by arxiv id')
        parser.add_argument('-t', '--title', nargs='*', type=str, default=[], help='search by words in title')
        parser.add_argument('-au', '--author', nargs='*', type=str, default=[], help='search by parts of author name')
        parser.add_argument('-ab', '--abstract', nargs='*', type=str, default=[], help='search by words in abstract')
        return parser

    @staticmethod
    def create_search_args(args: ap.Namespace) -> dict:
        """Returns a dictionary of keyword arguments created from the given Namespace of parsed user args, intended to
        use as the default settings for instantiation an instance of a query class (BaseQuery subclass)
        :param args: parsed user arguments
        :return: default keyword arguments for creating a Query class
        """
        return {
            'title_args': args.title + args.all,
            'id_args': args.arvix_id + args.all,
            'abstract_args': args.abstract + args.all,
            'author_args': args.author + args.all
        }

    @classmethod
    def from_args(cls: type):
        """Asks the user for a list of arguments, creating an instance of this BaseQuery (or subclass) from them.
        Doesn't exit or throw an error if invalid arguments are entered or if user asks for help
        :param cls: the type of the class being created (BaseQuery of subclass)
        :return: instantiated class of given type"""
        parser = cls.get_parser()
        while True:
            try:
                args = u.get_formatted_user_input('enter search params')
                args = parser.parse_args(args)
                print('fetching results...')
                return cls(**cls.create_search_args(args))
            except ArgumentParserException as e:  # invalid args, try again than error out
                print(e)
            except SystemExit:  # if help requested, don't system exit
                pass
