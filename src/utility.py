from typing import Any, List, Iterable
import enum as e
import abc
import argparse as ap
import dataclasses as dc


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
    def get_parser() -> ap.ArgumentParser:
        parser = ap.ArgumentParser()
        parser.add_argument('-id', '--arvix_id', nargs='*', type=str, default=[])
        parser.add_argument('-t', '--title', nargs='*', type=str, default=[])
        parser.add_argument('-a', '--author', nargs='*', type=str, default=[])
        parser.add_argument('-ab', '--abstract', nargs='*', type=str, default=[])
        return parser

    @classmethod
    def from_params(cls: type, params: List[str]):
        parser = BaseQuery.get_parser()
        args = parser.parse_args(params)
        return cls(title_params=args.title, id_params=args.arvix_id,
                   abstract_params=args.abstract, author_params=args.author)


class EqualEnum(e.Enum):
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
    def values_as_str(cls: type) -> str:
        return ', '.join(item.value for item in cls)


def is_list_of_n_ints(to_parse: List[str], n: int = -1) -> List[int]:
    if not to_parse:
        return []
    elif n > -1 and len(to_parse) != n:  # -1 means variable length
        raise ValueError(f'given list {to_parse} must have only {n} entries')

    for idx, entry in enumerate(to_parse):
        to_parse[idx] = int(entry)
    return to_parse


if __name__ == '__main__':
    class Foo(EqualEnum):
        A = 'A'
        B = 'B'


    assert Foo.is_valid('A')
    assert Foo.is_valid('B')
    print(Foo.values_as_str())
