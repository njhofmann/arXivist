from __future__ import annotations
from typing import Any, List, Final
import dataclasses as dc
import pathlib as pl


def split_and_format_string(to_format: str) -> List[str]:
    """
    Splits a string on any spaces in the string, removes any reuslting empty strings, and returns a list of the split
    string.
    :param to_format: string to format
    :return: split string
    """
    return [char for char in to_format.split(' ') if char]


@dc.dataclass
class SearchResult:
    """Represents a paper retrieved as a result of a query to the database or directly from arXiv itself"""
    id: str  # paper's arxiv id
    authors: List[str]  # authors of paper in terms of listed authorship
    keywords: List[str]  # keywords assigned to this paper for retrieval in the database
    title: str = ''  # title of paper
    abstract: str = ''  # summary of the paper
    publish: str = ''  # date this paper was published
    pdf_url: str = ''  # url from which this paper's pdf can be retrieved
    pdf_path: pl.Path = ''  # path to the downloaded pdf of this paper

    def __str__(self):
        return f"Title: {self.title}\nAuthors: {', '.join(self.authors)}\nAbstract: {self.abstract}"

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, SearchResult) and self.id == other.id

    def add_author(self, author: str) -> None:
        if self.authors:
            self.authors.append(author)
        else:
            self.authors = [author]

    def add_keyword(self, keyword: str) -> None:
        if self.keywords:
            self.keywords.append(keyword)
        else:
            self.keywords = [keyword]
