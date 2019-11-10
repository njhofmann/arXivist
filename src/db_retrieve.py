import psycopg2 as psy
from psycopg2 import sql
from typing import List, Tuple, Iterable, Dict
import utility as u


class DatabaseQuery(u.BaseQuery):

    def __init__(self, title_params: Iterable[str] = (), author_params: Iterable[str] = (),
                 abstract_params: Iterable[str] = (), id_params: Iterable[str] = (),
                 max_result: int = 10, start: int = 0) -> None:
        super().__init__(title_params=title_params, author_params=author_params, abstract_params=abstract_params,
                         id_params=id_params, max_result=max_result, start=start)

    def format_params(self, params: Iterable[str]):
        formatted_params = [f'{{}} LIKE "%{param}%"' for param in params]
        return ' AND '.join(formatted_params)

    def as_sql_query(self):
        columns_to_params = {'arvix_id': self.id_params, 'abstract': self.abstract_params, 'title': self.title_params,
                             'author': self.author_params}

        columns_to_formatted_params = {column: self.format_params(params)
                                       for column, params in columns_to_params.items()}
        query = sql.SQL('SELECT {}, {}, {}, {}, {} FROM {} {}, {}, {} WHERE {} = {}')
        query = None

    def aggregate_results(self, results: List[Tuple[str, str, str, str, str]]) -> List[u.SearchResult]:
        search_results: Dict[str, u.SearchResult] = {}
        for result in results:
            arxiv_id, title, abstract, pdf_path, author = result
            if arxiv_id in search_results:
                search_results.get(arxiv_id)

    def get_results(self, cursor) -> List[Tuple[int, u.SearchResult]]:
        with psy.connect(dbname='arxiv') as conn:
            with conn.cursor() as cursor:
                cursor.execute(self.as_sql_query())
                results = cursor.fetchall()

        search_results = self.aggregate_results(results)
        count = self.start
        while count < search_results:
            pass




def get_suggestions(cursor) -> List[Tuple[str]]:
    query = sql.SQL('WITH {} AS (SELECT DISTINCT({}) {} FROM {}) '
                    'SELECT {} {} FROM {} {}, {}, {} WHERE {} NOT IN {} GROUP BY {} ORDER BY COUNT(*) ').format(
        sql.Identifier('added_ids'), sql.Identifier('child_id'), sql.Identifier('id'), sql.Identifier('citation_graph'),
        sql.Identifier('p', 'parent_id'), sql.Identifier('pi'), sql.Identifier('citation_graph'), sql.Identifier('p'),
        sql.Identifier('added_ids'), sql.Identifier('a'), sql.Identifier('pi'), sql.Identifier('a', 'id'),
        sql.Identifier('pi'))
    print()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == '__main__':
    get_suggestions()
