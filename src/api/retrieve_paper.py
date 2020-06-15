import requests as r
from typing import Iterable, List, Tuple
import itertools as i
import xml.etree as xe
import src.utility.search_result as sr
import xml.etree.ElementTree as xee
import src.utility.base_query as bq


class SearchQuery(bq.BaseQuery):
    BASE_QUERY_URL = 'http://export.arxiv.org/api/query/?'
    BASE_ARXIV_URL = 'http://arxiv.org/abs/'
    XML_ATOM_ROOT = '{http://www.w3.org/2005/Atom}'
    XML_OPEN_SEARCH_ROOT = '{http://a9.com/-/spec/opensearch/1.1/}'

    def __init__(self, title_params: Iterable[str] = (), author_params: Iterable[str] = (),
                 abstract_params: Iterable[str] = (), id_params: Iterable[str] = (),
                 max_result: int = 10, start: int = 0) -> None:
        super().__init__(title_params=title_params, author_params=author_params, abstract_params=abstract_params,
                         id_params=id_params, max_result=max_result, start=start)
        search_codes_to_params = {'ti': title_params, 'au': author_params, 'abs': abstract_params}

        id_params = ('id_list=' + ','.join(id_params)) if id_params else ''

        formatted_params = list(i.chain.from_iterable([[f'{code}:{param}' for param in params]
                                                       for code, params in search_codes_to_params.items()]))
        formatted_params = ('search_query=' + '+AND+'.join(formatted_params)) if formatted_params else ''

        if formatted_params and id_params:
            self.query = self.BASE_QUERY_URL + formatted_params + id_params
        elif id_params or formatted_params:
            self.query = self.BASE_QUERY_URL + (id_params if id_params else formatted_params)

    def get_response_with_limited_query(self, start: int, space: int) -> r.Response:
        return r.get(self.query + f'&start={start}&max_result={space}')

    def get_response_with_starting_query(self) -> r.Response:
        return self.get_response_with_limited_query(self.start, self.max_result)

    def get_xml_tree(self, text: str) -> xe.ElementTree:
        return xe.ElementTree.fromstring(text)

    def retrieve_search_results(self) -> List[Tuple[int, sr.SearchResult]]:
        response = self.get_response_with_starting_query()
        if response.ok:  # ok, begin recursive parsing
            root = self.get_xml_tree(response.text)
            total_results = int(self.get_open_search_child(root, 'totalResults').text)
            return self.retrieve_valid_search_results(self.start, self.max_result, total_results)
        return self.parse_error(response.text)

    def retrieve_valid_search_results(self, start: int, space: int, end: int) -> List[Tuple[int, sr.SearchResult]]:
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

    def parse_valid_response(self, xml_response: str) -> List[sr.SearchResult]:
        root = self.get_xml_tree(xml_response)
        entries = self.get_atom_children(root, 'entry')
        parsed_entries = []
        for entry in entries:
            title = self.get_atom_child_text(entry, 'title')

            arxiv_id = self.get_atom_child_text(entry, 'id')
            if arxiv_id.startswith(self.BASE_ARXIV_URL):
                arxiv_id = arxiv_id[len(self.BASE_ARXIV_URL):]

            abstract = self.get_atom_child_text(entry, 'summary')

            date = self.get_atom_child_text(entry, 'published')
            updated_dates = self.get_atom_children(entry, 'updated')
            if updated_dates:
                date = updated_dates[-1].text

            pdf_link = None
            for link in self.get_atom_children(entry, 'link'):
                if link.get('title'):
                    pdf_link = link.get('href')
                    break

            authors = [self.get_atom_child(author, 'name').text for author in self.get_atom_children(entry, 'author')]

            parsed_entries.append(sr.SearchResult(title=title, id=arxiv_id, abstract=abstract, authors=authors,
                                                 pdf_url=pdf_link, publish=date, keywords=[]))
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
    print(list(results))
