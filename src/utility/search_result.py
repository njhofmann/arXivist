from __future__ import annotations
import dataclasses as dc
import pathlib as pl
from typing import Any, List, Set


@dc.dataclass
class SearchResult:
    """Represents a paper retrieved as a result of a query to the database or directly from arXiv itself"""
    id: str  # paper's arxiv id
    authors: List[str]  # authors of paper in terms of listed authorship
    keywords: Set[str]  # keywords assigned to this paper for retrieval in the database
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
            self.keywords.add(keyword)
        else:
            self.keywords = {keyword}
