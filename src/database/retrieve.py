from typing import List, Tuple, Iterable, Dict

import psycopg2 as psy
from psycopg2 import sql

import src.db_util as db
import src.utility.base_query as bq
import src.utility.search_result as sr

"""Module containing classes and functions relating to retrieving data from the database"""


class DatabaseQuery(bq.BaseQuery):

    def __init__(self, title_params: Iterable[str] = (), author_params: Iterable[str] = (),
                 abstract_params: Iterable[str] = (), id_params: Iterable[str] = (),
                 max_result: int = 10, start: int = 0) -> None:
        super().__init__(title_params=title_params, author_params=author_params, abstract_params=abstract_params,
                         id_params=id_params, max_result=max_result, start=start)
        
    @staticmethod
    def format_params(params: Iterable[str]) -> str:
        formatted_params = [f'LOWER({{}}) LIKE \'%{param.lower()}%\'' for param in params]
        return ' AND '.join(formatted_params)
    
    @staticmethod
    def n_column_identifiers(table: str, column: str, n: int) -> List[sql.Identifier]:
        if n < 1:
            return []
        return [sql.Identifier(table, column) for _ in range(n)]

    def as_sql_query(self):
        cols_to_params = {'arvix_id': self.id_params, 'abstract': self.abstract_params, 'title': self.title_params,
                             'author': self.author_params}

        col_to_formatted_params = {col: self.format_params(params) for col, params in cols_to_params.items()}

        columns_to_identifiers = {}
        for column, params in cols_to_params.items():
            table = 'pa' if column == 'author' else 'pi'
            n = len(params)
            columns_to_identifiers[column] = self.n_column_identifiers(table, column, n)

        base_query = 'SELECT {}, {}, {}, {}, {} FROM {} {} JOIN {} {} ON {} = {}'
        base_identifiers = [sql.Identifier('pi', 'arxiv_id'), sql.Identifier('pi', 'title'),
                            sql.Identifier('pi', 'abstract'),
                            sql.Identifier('pi', 'pdf_path'), sql.Identifier('pa', 'author'),
                            sql.Identifier('paper_info'),
                            sql.Identifier('pi'), sql.Identifier('paper_author'), sql.Identifier('pa'),
                            sql.Identifier('pi', 'arxiv_id'), sql.Identifier('pa', 'arxiv_id')]

        formatted_params = ''
        for column, identifiers in columns_to_identifiers.items():
            if identifiers:
                formatted_params += (' AND ' if formatted_params else '') + col_to_formatted_params[column]
                base_identifiers.extend(identifiers)

        if formatted_params:
            base_query += ' WHERE ' + formatted_params

        full_query = sql.SQL(base_query).format(*base_identifiers)
        return full_query

    def aggregate_results(self, results: List[Tuple[str, str, str, str, str]]) -> List[sr.SearchResult]:
        search_results: Dict[str, sr.SearchResult] = {}
        for result in results:
            arxiv_id, title, abstract, pdf_path, author = result
            if arxiv_id in search_results:
                search_results.get(arxiv_id).add_author(author)
            else:
                search_results[arxiv_id] = sr.SearchResult(title=title, pdf_path=pdf_path, abstract=abstract,
                                                           authors=[author], id=arxiv_id)
        return list(search_results.values())

    def get_results(self) -> List[Tuple[int, sr.SearchResult]]:

        def execute(cursor):
            cursor.execute(self.as_sql_query())
            return cursor.fetchall()

        results = db.generic_db_query(execute)
        search_results = self.aggregate_results(results)
        count = self.start
        while count < len(search_results):
            gen_results = search_results[count:count + self.max_result]
            yield [(count + idx, result) for idx, result in enumerate(gen_results)]
            count += self.max_result


def get_suggestions(cursor) -> List[str]:
    query = sql.SQL('WITH {} AS (SELECT DISTINCT({}) {} FROM {}) '
                    'SELECT {} FROM {} {}, {} {} WHERE {} != {} GROUP BY {} ORDER BY COUNT(*) ').format(
        sql.Identifier('added_ids'), sql.Identifier('child_id'), sql.Identifier('id'), sql.Identifier('citation_graph'),
        sql.Identifier('p', 'parent_id'), sql.Identifier('citation_graph'), sql.Identifier('p'),
        sql.Identifier('added_ids'), sql.Identifier('a'), sql.Identifier('p', 'parent_id'), sql.Identifier('a', 'id'),
        sql.Identifier('p', 'parent_id'))
    cursor.execute(query)
    return list(map(lambda x: x[0], cursor.fetchall))


def get_suggested_papers() -> List[str]:
    return db.generic_db_query(get_suggestions)


if __name__ == '__main__':
    get_suggestions()
