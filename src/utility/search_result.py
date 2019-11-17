from __future__ import annotations
from typing import Any, List
import dataclasses as dc


def split_and_format_string(to_format: str) -> List[str]:
    to_format = to_format.split(' ')
    return [char for char in to_format if char]


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
