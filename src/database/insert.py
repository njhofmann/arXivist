import pathlib as pl
from typing import Dict, List

from psycopg2 import sql

import src.utility.search_result as u

"""Module containing functionality for inserting data into the database"""


def execute_insertion(cursor, table: str, column_to_value: Dict[str, str]) -> None:
    blank_columns = ', '.join(['{}' for _ in column_to_value])
    blank_values = ', '.join(['%s' for _ in column_to_value])
    columns = [sql.Identifier(column) for column in column_to_value.keys()]

    query = sql.SQL(f'INSERT INTO {{}} ({blank_columns}) VALUES ({blank_values})').format(
        sql.Identifier(table), *columns)
    cursor.execute(query, tuple(column_to_value.values()))


def insert_paper_info(cursor, paper_id: str, title: str, abstract: str, publish_date: str, pdf_link: str,
                      pdf_path: pl.Path) -> None:
    columns_to_values = {'arxiv_id': paper_id, 'title': title, 'abstract': abstract, 'published': publish_date,
                         'pdf_link': pdf_link, 'pdf_path': str(pdf_path)}
    execute_insertion(cursor, 'paper_info', columns_to_values)


def insert_search_query(cursor, search_query: u.SearchResult, references: List[str], pdf_path: pl.Path) -> None:
    insert_paper_info(cursor, paper_id=search_query.id, abstract=search_query.abstract,
                      publish_date=search_query.publish, pdf_link=search_query.pdf_url,
                      title=search_query.title, pdf_path=pdf_path)

    insert_authors(cursor, search_query.id, search_query.authors)
    insert_citations(cursor, search_query.id, references)
    insert_keywords(cursor, search_query.id, search_query.keywords)


def insert_authors(cursor, paper_id: str, authors: List[str]) -> None:
    for author in authors:
        columns_to_values = {'arxiv_id': paper_id, 'author': author}
        execute_insertion(cursor, 'paper_author', columns_to_values)


def insert_citations(cursor, paper_id: str, references: List[str]) -> None:
    for reference in references:
        columns_to_values = {'child_id': paper_id, 'parent_id': reference}
        execute_insertion(cursor, 'citation_graph', columns_to_values)


def insert_keywords(cursor, paper_id: str, keywords: List[str]) -> None:
    for keyword in keywords:
        columns_to_values = {'arxiv_id': paper_id, 'keyword': keyword}
        execute_insertion(cursor, 'paper_keyword', columns_to_values)


if __name__ == '__main__':
    execute_insertion(None, 'foo', {'bar': 'baz', 'gar': 'gaz'})
