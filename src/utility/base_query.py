import abc
import argparse as ap
from typing import Iterable, List


class ArgumentParserException(Exception):
    pass


class RaisingArgParser(ap.ArgumentParser):
    """Custom ArgumentParser class that raises exceptions instead of exiting the system."""

    def error(self, msg: str):
        raise ArgumentParserException(msg)


class BaseQuery(abc.ABC):

    def __init__(self, title_args: Iterable[str] = (), author_args: Iterable[str] = (),
                 abstract_args: Iterable[str] = (), id_args: Iterable[str] = (),
                 max_result: int = 10, start: int = 0) -> None:
        if not any([title_args, author_args, abstract_args, id_args]):
            raise ValueError('must be given one or more args')

        self.title_args = title_args
        self.author_args = author_args
        self.abstract_args = abstract_args
        self.id_args = id_args
        self.max_result = max_result
        self.start = start

    @staticmethod
    def get_parser() -> RaisingArgParser:
        """Returns an ArgumentParser for creating a BaseQuery
        :return: custom ArgumentParser
        """
        # TODO search by keyword..?
        parser = RaisingArgParser(prefix_chars='-', description='parse paper search arguments')
        parser.add_argument('-a', '--all', nargs='*', type=str, default=[], help='apply argument to each other arg')
        parser.add_argument('-id', '--arvix_id', nargs='*', type=str, default=[], help='search by arxiv id')
        parser.add_argument('-t', '--title', nargs='*', type=str, default=[], help='search by words in title')
        parser.add_argument('-au', '--author', nargs='*', type=str, default=[], help='search by parts of author name')
        parser.add_argument('-ab', '--abstract', nargs='*', type=str, default=[], help='search by words in abstract')
        return parser

    @classmethod
    def from_args(cls: type, args: List[str]):
        """Given a list of arguments, creates an instance of this BaseQuery (or subclass)
        :param cls: the type of the class being created (BaseQuery of subclass)
        :param args: list of arguments to create the class from
        :return: instantiated class of given type"""
        parser = BaseQuery.get_parser()
        args = parser.parse_args(args)
        return cls(title_args=args.title + args.all,
                   id_args=args.arvix_id + args.all,
                   abstract_args=args.abstract + args.all,
                   author_args=args.author + args.all)
