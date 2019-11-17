import requests as r
from utility import search_result as u
from typing import List
import json as j
import re

ARXIV_VERSION = re.compile('v[0-9]')
BASE_URL = 'http://api.semanticscholar.org/v1/paper/arXiv:'


def get_arxiv_url(result: str) -> str:
    if ARXIV_VERSION.match(result, len(result) - 2):
        result = result[:-2]
    return BASE_URL + result


def retrieve_references(search_result: u.SearchResult) -> List[str]:
    response = r.get(get_arxiv_url(search_result.id))
    if response.ok:
        references = j.loads(response.content)['references']
        return [reference['arxivId'] for reference in references if reference['arxivId']]
    else:
        response.raise_for_status()


if __name__ == '__main__':
    print(retrieve_references(u.SearchResult(title='test', authors=[], pdf_url='foo', abstract='foo', id='1509.06461')))

