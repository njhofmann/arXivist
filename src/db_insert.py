from psycopg2 import sql
import utility as u
from typing import Dict, List
import pathlib as pl


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

