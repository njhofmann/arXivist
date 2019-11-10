import requests as r
from typing import Iterable, List, Tuple
import itertools as i
import dataclasses as dc
import xml.etree as xe
import xml.etree.ElementTree as xee
import argparse as ap


@dc.dataclass
class SearchResult:
    title: str
    id: str  # arxiv id
    abstract: str
    authors: List[str]  # authors of paper in terms of ordership
    pdf_link: str

    def __str__(self):
        return f"""
        Title: {self.title}\n
        Authors: {','.join(self.authors)}\n
        Abstract: {self.abstract}
        """


class SearchQuery:

    BASE_QUERY_URL = 'http://export.arxiv.org/api/query/?'
    BASE_ARXIV_URL = 'http://arxiv.org/abs/'
    XML_ATOM_ROOT = '{http://www.w3.org/2005/Atom}'
    XML_OPEN_SEARCH_ROOT = '{http://a9.com/-/spec/opensearch/1.1/}'

    def __init__(self, title_params: Iterable[str] = (), author_params: Iterable[str] = (),
                 abstract_params: Iterable[str] = (), id_params: Iterable[str] = (),
                 max_result: int = 10) -> None:
        search_codes_to_params = {'ti': title_params, 'au': author_params, 'abs': abstract_params}

        if not any([title_params, author_params, abstract_params, id_params]):
            raise ValueError('must be given one or more params')

        id_params = ('id_list=' + ','.join(id_params)) if id_params else ''

        formatted_params = list(i.chain.from_iterable([[f'{code}:{param}' for param in params]
                                                       for code, params in search_codes_to_params.items()]))
        formatted_params = ('search_query=' + '+AND+'.join(formatted_params)) if formatted_params else ''

        if formatted_params and id_params:
            self.query = self.BASE_QUERY_URL + formatted_params + id_params
        elif id_params or formatted_params:
            self.query = self.BASE_QUERY_URL + (id_params if id_params else formatted_params)

        self.max_result = max_result
        self.start = 0

    @staticmethod
    def get_parser() -> ap.ArgumentParser:
        parser = ap.ArgumentParser()
        parser.add_argument('-id', '--arvix_id', nargs='*', type=str, default=[])
        parser.add_argument('-t', '--title', nargs='*', type=str, default=[])
        parser.add_argument('-a', '--author', nargs='*', type=str, default=[])
        parser.add_argument('-ab', '--abstract', nargs='*', type=str, default=[])
        return parser

    @staticmethod
    def from_params(params: List[str]):
        parser = SearchQuery.get_parser()
        args = parser.parse_args(params)
        return SearchQuery(title_params=args.title, id_params=args.arvix_id,
                           abstract_params=args.abstract, author_params=args.author)

    def get_response_with_limited_query(self, start: int, space: int):
        return r.get(self.query + f'&start={start}&max_result={space}')

    def get_response_with_starting_query(self):
        return self.get_response_with_limited_query(self.start, self.max_result)

    def get_xml_tree(self, text: str) -> xe.ElementTree:
        return xe.ElementTree.fromstring(text)

    def retrieve_search_results(self) -> List[Tuple[int, SearchResult]]:
        response = self.get_response_with_starting_query()
        if response.ok:  # ok, begin recursive parsing
            root = self.get_xml_tree(response.text)
            total_results = int(self.get_open_search_child(root, 'totalResults').text)
            return self.retrieve_valid_search_results(self.start, self.max_result, total_results)
        return self.parse_error(response.text)

    def retrieve_valid_search_results(self, start: int, space: int, end: int) -> List[Tuple[int, SearchResult]]:
        count = 0
        while True:
            search_results = self.parse_valid_response(self.get_response_with_limited_query(start, space).text)

            for idx, result in enumerate(search_results):
                search_results[idx] = (count, result)
                count += 1
            yield search_results

            start += space
            if start > end:
                break

    def get_atom_child(self, parent: xee.Element, tag: str) -> xee.Element:
        return parent.find(self.XML_ATOM_ROOT + tag)

    def get_atom_child_text(self, parent: xee.Element, tag: str) -> str:
        return self.get_atom_child(parent, tag).text

    def get_atom_children(self, parent: xee.Element, tag: str) -> xee.Element:
        return parent.findall(self.XML_ATOM_ROOT + tag)

    def get_open_search_child(self, parent: xee.Element, tag: str) -> xee.Element:
        return parent.find(self.XML_OPEN_SEARCH_ROOT + tag)

    def parse_valid_response(self, xml_response: str) -> List[SearchResult]:
        root = self.get_xml_tree(xml_response)
        entries = self.get_atom_children(root, 'entry')
        parsed_entries = []
        for entry in entries:
            title = self.get_atom_child_text(entry, 'title')

            arxiv_id = self.get_atom_child_text(entry, 'id')
            if arxiv_id.startswith(self.BASE_ARXIV_URL):
                arxiv_id = arxiv_id[len(self.BASE_ARXIV_URL):]

            abstract = self.get_atom_child_text(entry, 'summary')

            pdf_link = None
            for link in self.get_atom_children(entry, 'link'):
                if link.get('title'):
                    pdf_link = link.get('href')
                    break

            authors = [self.get_atom_child(author, 'name').text for author in self.get_atom_children(entry, 'author')]

            parsed_entries.append(SearchResult(title=title, id=arxiv_id, abstract=abstract, authors=authors, pdf_link=pdf_link))
        return parsed_entries

    def parse_error(self, error_msg: str):
        root = xe.ElementTree.fromstring(error_msg)
        entry = self.get_atom_child(root, 'entry')
        return self.get_atom_child(entry, 'summary').text

    def __str__(self):
        return self.query


if __name__ == '__main__':
    url = SearchQuery(title_params=['learning', 'reinforcement', 'deep', 'replay'])
    print(url)
    results = url.retrieve_search_results()
    print(results)
