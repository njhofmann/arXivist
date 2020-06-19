from __future__ import annotations
from typing import Set, Dict
import src.api.retrieve_biblio as rb
import src.database.insert as dbi
import src.db_util as dbu
import src.pdf_utils as pu
import src.utility.search_result as sr


class SaveQuery:

    def __init__(self):
        self.selected_ids: Set[int] = set()
        self.valid_ids_to_info: Dict[int, sr.SearchResult] = {}

    def add_valid_id(self, result_id: int, result: sr.SearchResult) -> None:
        if result_id in self.valid_ids_to_info:
            raise ValueError(f'id {result_id} already added to list of valid ids')
        # TODO fix type error
        self.valid_ids_to_info[result_id] = result

    def get_result(self, result_id: int) -> sr.SearchResult:
        if self.is_valid_id(result_id):
            return self.valid_ids_to_info[result_id]
        raise ValueError(f'id {result_id} is not a valid id')

    def select_id(self, param: int) -> None:
        if not self.is_valid_id(param):
            raise ValueError(f'{param} not in list of valid ids')
        self.selected_ids.add(param)

    def is_valid_id(self, result_id: int) -> bool:
        return result_id in self.valid_ids_to_info

    def __str__(self):
        if self.selected_ids:
            return f"save query: {', '.join([str(entry) for entry in self.selected_ids])}"
        return 'nothing in save query'

    def submit(self) -> None:
        for result_id in self.selected_ids:
            result = self.get_result(result_id)
            pdf_path = pu.fetch_and_save_pdf(result)
            references = rb.retrieve_references(result)
            dbu.generic_db_query(dbi.insert_search_query, result, references, pdf_path)
