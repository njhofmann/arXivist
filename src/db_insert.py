import psycopg2 as psy
from psycopg2 import sql

import pdf_utils as rpdf
import retrieve_biblio as rb
import retrieve_paper as rp
import utility as u
from typing import Dict, List, Set
import pathlib as pl
from utility import SearchResult


def get_generic_insertion(cursor, table: str, column_to_value: Dict[str, str]) -> None:
    blank_columns = ', '.join(['{}' for _ in column_to_value])
    blank_values = ', '.join(['%s' for _ in column_to_value])
    columns = [sql.Identifier(column) for column in column_to_value.keys()]

    query = sql.SQL(f'INSERT INTO {{}} ({blank_columns}) VALUES ({blank_values})').format(
        sql.Identifier(table), *columns)
    cursor.execute(query, tuple(column_to_value.values()))


def insert_paper_author(cursor, paper_id: str, author: str) -> None:
    columns_to_values = {'arxiv_id': paper_id, 'author': author}
    get_generic_insertion(cursor, 'paper_author', columns_to_values)


def insert_paper_info(cursor, paper_id: str, title: str, abstract: str, publish_date: str, pdf_link: str,
                      pdf_path: pl.Path) -> None:
    columns_to_values = {'arxiv_id': paper_id, 'title': title, 'abstract': abstract, 'published': publish_date,
                         'pdf_link': pdf_link, 'pdf_path': str(pdf_path)}
    get_generic_insertion(cursor, 'paper_info', columns_to_values)


def insert_search_query(cursor, search_query: u.SearchResult, references: List[str], pdf_path: pl.Path) -> None:
    insert_paper_info(cursor, paper_id=search_query.id, abstract=search_query.abstract,
                      publish_date=search_query.publish, pdf_link=search_query.pdf_url,
                      title=search_query.title, pdf_path=pdf_path)

    for author in search_query.authors:
        insert_paper_author(cursor, search_query.id, author)

    for reference in references:
        insert_paper_references(cursor, search_query.id, reference)


def insert_paper_references(cursor, paper_id: str, reference: str) -> None:
    columns_to_values = {'child_id': paper_id, 'parent_id': reference}
    get_generic_insertion(cursor, 'citation_graph', columns_to_values)


if __name__ == '__main__':
    get_generic_insertion(None, 'foo', {'bar': 'baz', 'gar': 'gaz'})


class SaveQuery:

    def __init__(self):
        self.selected_ids: Set[int] = set()
        self.valid_ids_to_info: Dict[int, SearchResult] = {}

    def add_valid_id(self, result_id: int, result: rp.SearchQuery) -> None:
        if result_id in self.valid_ids_to_info:
            raise ValueError(f'id {result_id} already added to list of valid ids')
        self.valid_ids_to_info[result_id] = result

    def get_result(self, result_id: int) -> SearchResult:
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
        with psy.connect(dbname='arxiv') as conn:
            with conn.cursor() as cursor:
                for result_id in self.selected_ids:
                    result = self.get_result(result_id)
                    pdf_path = rpdf.fetch_and_save_pdf(result)
                    references = rb.retrieve_references(result)
                    dbe.insert_search_query(cursor, result, references, pdf_path)