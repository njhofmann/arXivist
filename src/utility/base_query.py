import abc
import argparse as ap
from typing import Iterable, List


class ArgumentParserException(Exception):
    pass


class RaisingArgParser(ap.ArgumentParser):
    """Custom ArggumentParser class that raises exceptions instead of exiting the system."""

    def error(self, msg: str):
        raise ArgumentParserException(msg)


class BaseQuery(abc.ABC):

    def __init__(self, title_params: Iterable[str] = (), author_params: Iterable[str] = (),
                 abstract_params: Iterable[str] = (), id_params: Iterable[str] = (),
                 max_result: int = 10, start: int = 0) -> None:
        if not any([title_params, author_params, abstract_params, id_params]):
            raise ValueError('must be given one or more params')

        self.title_params = title_params
        self.author_params = author_params
        self.abstract_params = abstract_params
        self.id_params = id_params
        self.max_result = max_result
        self.start = start

    @staticmethod
    def get_parser() -> RaisingArgParser:
        parser = RaisingArgParser(prefix_chars='-')
        parser.add_argument('-a', '--all', nargs='*', type=str, default=[])
        parser.add_argument('-id', '--arvix_id', nargs='*', type=str, default=[])
        parser.add_argument('-t', '--title', nargs='*', type=str, default=[])
        parser.add_argument('-au', '--author', nargs='*', type=str, default=[])
        parser.add_argument('-ab', '--abstract', nargs='*', type=str, default=[])
        return parser

    @classmethod
    def from_params(cls: type, params: List[str]):
        parser = BaseQuery.get_parser()
        args = parser.parse_args(params)
        return cls(title_params=args.title + args.all,
                   id_params=args.arvix_id + args.all,
                   abstract_params=args.abstract + args.all,
                   author_params=args.author + args.all)
