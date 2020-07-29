from __future__ import annotations

from typing import Generator, List, Tuple

import src.api.retrieve_paper as rp
import src.database.retrieve as dbr
import src.modes.search_options as so
import src.utility.search_result as sr

"""Module for suggesting new papers to a user based on previously saved papers."""


def suggest_mode_retrieval() -> Generator[List[Tuple[int, sr.SearchResult]], None, None]:
    print('entered suggest mode')
    suggested_ids = dbr.get_suggested_papers()
    return rp.SearchQuery(id_args=suggested_ids).retrieve_search_results()


def suggest_mode() -> None:
    so.generic_search_mode(suggest_mode_retrieval)
