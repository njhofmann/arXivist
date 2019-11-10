import requests as r
from retrieve_paper import SearchResult
from typing import List
import json as j

BASE_URL = 'http://api.semanticscholar.org/v1/paper/arXiv:'


def get_arxiv_url(result: str) -> str:
    return BASE_URL + result


def retrieve_references(search_result: SearchResult) -> List[str]:
    response = r.get(get_arxiv_url(search_result.id))
    if response.ok:
        references = j.loads(response.content)['references']
        return [reference['arxivId'] for reference in references if reference['arxivId']]
    else:
        response.raise_for_status()


if __name__ == '__main__':
    print(retrieve_references(SearchResult(title='test', authors=[], pdf_link='foo', abstract='foo', id='1509.06461')))

