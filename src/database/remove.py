from typing import Tuple, Union

import psycopg2 as psy
from psycopg2 import sql

import src.db_util as dbi

"""Module containing functionalities relating to remove data from the database"""


def generic_execution(query: sql.Composed, params: Tuple[Union[str, int], ...]) -> None:
    db_info = dbi.get_db_info()
    with psy.connect(user=db_info.user, password=db_info.password, dbname=db_info.db_name) as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)


def remove_paper(arxiv_id: int) -> None:
    """
    Removes paper with the given arXiv ID, and all related entries, from the database.
    :param arxiv_id: id of paper to remove
    :param cursor: cursor of the database
    :return: None
    """
    query = sql.SQL('DELETE FROM {} WHERE {} = %s').format(
        sql.Identifier('paper_info'), sql.Identifier('arxiv_id'))
    generic_execution(query, (arxiv_id,))


def remove_keyword(arxiv_id: str, keyword: str) -> None:
    """
    Removes the keyword associated with the given paper (by arXiv ID) from the database using the given cursor
    associated with the database
    :param arxiv_id: arXiv ID of the associated paper
    :param keyword: keyword of the paper to remove
    :param cursor: cursor the associated database
    :return: None
    """
    query = sql.SQL('DELETE FROM {} WHERE {} = %s AND WHERE {} = %s').format(
        sql.Identifier('paper_info'), sql.Identifier('arxiv_id'), sql.Identifier('keyword'))
    generic_execution(query, (arxiv_id, keyword))
