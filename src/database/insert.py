import pathlib as pl
from typing import Dict, List, Iterable
from psycopg2 import sql
import src.utility.search_result as u

"""Module containing functionality for inserting data into the database"""


def execute_insertion(cursor, table: str, col_to_value: Dict[str, str]) -> None:
    blank_cols = ', '.join(['{}' for _ in col_to_value])
    blank_vals = ', '.join(['%s' for _ in col_to_value])
    cols = [sql.Identifier(col) for col in col_to_value.keys()]

    query = sql.SQL(f'INSERT INTO {{}} ({blank_cols}) VALUES ({blank_vals})').format(sql.Identifier(table), *cols)
    cursor.execute(query, tuple(col_to_value.values()))


def insert_paper_info(cursor, paper_id: str, title: str, abstract: str, publish_date: str, pdf_link: str,
                      pdf_path: pl.Path) -> None:
    cols_to_values = {'arxiv_id': paper_id, 'title': title, 'abstract': abstract, 'published': publish_date,
                         'pdf_link': pdf_link, 'pdf_path': str(pdf_path)}
    execute_insertion(cursor, 'paper_info', cols_to_values)


def insert_search_query(cursor, search_query: u.SearchResult, refs: List[str], pdf_path: pl.Path) -> None:
    insert_paper_info(cursor, paper_id=search_query.id, abstract=search_query.abstract,
                      publish_date=search_query.publish, pdf_link=search_query.pdf_url,
                      title=search_query.title, pdf_path=pdf_path)

    insert_authors(cursor, search_query.id, search_query.authors)
    insert_citations(cursor, search_query.id, refs)
    insert_keywords(cursor, search_query.id, search_query.keywords)


def insert_authors(cursor, paper_id: str, authors: List[str]) -> None:
    for author in authors:
        cols_to_values = {'arxiv_id': paper_id, 'author': author}
        execute_insertion(cursor, 'paper_author', cols_to_values)


def insert_citations(cursor, paper_id: str, refs: List[str]) -> None:
    for ref in refs:
        cols_to_values = {'child_id': paper_id, 'parent_id': ref}
        execute_insertion(cursor, 'citation_graph', cols_to_values)


def insert_keywords(cursor, paper_id: str, keywords: Iterable[str]) -> None:
    for keyword in keywords:
        cols_to_values = {'arxiv_id': paper_id, 'keyword': keyword}
        execute_insertion(cursor, 'paper_keyword', cols_to_values)


if __name__ == '__main__':
    execute_insertion(None, 'foo', {'bar': 'baz', 'gar': 'gaz'})
