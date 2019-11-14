from __future__ import annotations
from typing import Any, List, Iterable, Set, Dict
import enum as e
import abc
import argparse as ap
import dataclasses as dc
import psycopg2 as psy
import db_insert as dbe
import pdf_utils as rpdf
import retrieve_biblio as rb
import retrieve_paper as rp


def split_and_format_string(to_format: str) -> List[str]:
    to_format = to_format.split(' ')
    return [char for char in to_format if char]


class ArgumentParserException(Exception):
    pass


class RaisingArgParser(ap.ArgumentParser):
    """Custom ArggumentParser class that raises exceptions instead of exiting the system."""

    def error(self, msg: str):
        raise ArgumentParserException(msg)


class SaveQuery:

    def __init__(self):
        self.selected_ids: Set[int] = set()
        self.valid_ids_to_info: Dict[int, u.SearchResult] = {}

    def add_valid_id(self, result_id: int, result: rp.SearchQuery) -> None:
        if result_id in self.valid_ids_to_info:
            raise ValueError(f'id {result_id} already added to list of valid ids')
        self.valid_ids_to_info[result_id] = result

    def get_result(self, result_id: int) -> u.SearchResult:
        if self.is_valid_id(result_id):
            return self.valid_ids_to_info[result_id]
        raise ValueError(f'id {result_id} is not a valid id')

    def select_id(self, param: int) -> None:
        if not self.is_valid_id(param):
            raise ValueError(f'{param} not in list of valid ids')
        self.selected_ids.add(param)

    def is_valid_id(self, result_id: int) -> bool:
        return result_id in self.valid_ids_to_info

    def __str__(self):
        if self.selected_ids:
            return f"save query: {', '.join([str(entry) for entry in self.selected_ids])}"
        return 'nothing in save query'

    def submit(self) -> None:
        with psy.connect(dbname='arxiv') as conn:
            with conn.cursor() as cursor:
                for result_id in self.selected_ids:
                    result = self.get_result(result_id)
                    pdf_path = rpdf.fetch_and_save_pdf(result)
                    references = rb.retrieve_references(result)
                    dbe.insert_search_query(cursor, result, references, pdf_path)


@dc.dataclass
class SearchResult:
    id: str  # arxiv id
    authors: List[str]  # authors of paper in terms of ordership
    title: str = ''
    abstract: str = ''
    publish: str = ''
    pdf_url: str = ''
    pdf_path: str = ''

    def __str__(self):
        return f"Title: {self.title}\nAuthors: {', '.join(self.authors)}\nAbstract: {self.abstract}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        return self.id == other

    def add_author(self, author: str) -> None:
        if self.authors:
            self.authors.append(author)
        else:
            self.authors = [author]


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
        parser = RaisingArgParser
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
        return cls(title_params=args.title + args.all, id_params=args.arvix_id + args.all,
                   abstract_params=args.abstract + args.all, author_params=args.author + args.all)


class CommandEnum(e.Enum, abc.ABC):
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, type(self)):
            return self is other
        elif isinstance(other, str):
            return other == self.value
        return False

    @classmethod
    def is_valid(cls: type, other: str) -> bool:
        return any([other == item.value for item in cls])

    @classmethod
    def values_as_str(cls: e.Enum) -> str:
        return ', '.join(item.value for item in cls)

    @classmethod
    @abc.abstractmethod
    def execute_params(cls, params: List[str], save_query: SaveQuery = None) -> CommandEnum:
        """
        Maps the relationship between each defined type of CommandEnum and associated operations. Given a list of
        parameters, a command and any relevant arguments, attempts to execute operations associated with command listed
        in the params, should be the first item in the list - ie "cmd arg1 ... argn". Throws ValueError if unsupported
        command is given or if incorrect args are given. Returns the type of CommandEnum that was executed.
        :param params: list of params to execute an operation associated with a type of CommandEnum
        :param save_query: optional param, used for storing any neccessary info related to previously retrieved info
        :return: type of CommandEnum executed
        """
        if not params:
            raise ValueError(f"not provided a response, must be one of {cls.values_as_str()}")

        cmd = params[0]
        if not cls.is_valid(cmd):
            raise ValueError(f"invalid response {cmd}, must be one of {cls.values_as_str()}")


def is_list_of_n_ints(to_parse: List[str], n: int = -1) -> List[int]:
    if not to_parse:
        return []
    elif n > -1 and len(to_parse) != n:  # -1 means variable length
        raise ValueError(f'given list {to_parse} must have only {n} entries')

    for idx, entry in enumerate(to_parse):
        to_parse[idx] = int(entry)
    return to_parse


if __name__ == '__main__':
    class Foo(CommandEnum):
        A = 'A'
        B = 'B'


    assert Foo.is_valid('A')
    assert Foo.is_valid('B')
    print(Foo.values_as_str())
