from __future__ import annotations

from typing import List, Tuple, Generator

import src.api.retrieve_paper as rp
import src.modes.search_options as so
import src.utility.search_result as sr

"""Mode for searching for and saving papers from arXiv."""


def search_mode_retrieval() -> Generator[List[Tuple[int, sr.SearchResult]], None, None]:
    print('search mode entered')
    search_query = rp.SearchQuery.from_args()
    print('results fetched')
    return search_query.retrieve_search_results()


def search_mode():
    so.generic_search_mode(search_mode_retrieval)
