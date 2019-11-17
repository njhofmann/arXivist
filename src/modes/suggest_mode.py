from __future__ import annotations
from typing import List
from database import retrieve as dbr
import psycopg2 as psy
import src.api.retrieve_paper as rp
import src.utility.save_query as sq
import src.utility.command_enum as ce


class UserSuggestOptions(ce.CommandEnum):
    ADD = 'add'
    CONT = 'cont'
    QUIT = 'quit'
    MORE = 'more'
    VIEW = 'view'

    @classmethod
    def execute_params(cls, params: List[str], save_query: sq.SaveQuery = None) -> UserSuggestOptions:
        super().execute_params(params, save_query)
        cmd, params = params[0], params[1:]

        if cmd == UserSuggestOptions.MORE:
            selected_id = save_query.command_enum.is_list_of_n_ints(params, 1)[0]
            if not save_query.is_valid_id(selected_id):
                raise ValueError(f'selected id {selected_id} is not a valid id')
            print(save_query.get_result(selected_id))
            return UserSuggestOptions.MORE

        elif cmd == UserSuggestOptions.ADD:
            ids = save_query.command_enum.is_list_of_n_ints(params)
            for result_id in ids:
                save_query.select_id(result_id)
            return UserSuggestOptions.ADD

        elif cmd == UserSuggestOptions.CONT:
            save_query.command_enum.is_list_of_n_ints(params, 0)
            return UserSuggestOptions.CONT

        elif cmd == UserSuggestOptions.QUIT:
            save_query.command_enum.is_list_of_n_ints(params, 0)
            save_query.submit()
            return UserSuggestOptions.QUIT

        else:  # must be view
            save_query.command_enum.is_list_of_n_ints(params, 0)
            print(save_query)
            return UserSuggestOptions.VIEW


def suggest_mode():

    with psy.connect(dbname='arxiv') as conn:
        with conn.cursor() as cursor:
            suggestion_ids = dbr.get_suggestions(cursor)

    search_query = rp.SearchQuery(id_params=suggestion_ids)
    results = search_query.retrieve_search_results()
    
    save_query = sq.SaveQuery()
    for response in results:
        time_to_quit = False
        for idx, result in response:
            save_query.add_valid_id(idx, result)
            print(idx, result.title)

        print("\noptions:\n"
              "- 'more id' to view more info\n"
              "- 'cont' to view more results\n"
              "- 'add ids' to add results\n"
              "- 'quit' to terminate viewing save selections")

        wait_on_user = True
        while wait_on_user:
            results_response = input('waiting...\n')
            results_response = [result for result in results_response.split(' ') if result]
            cmd = UserSuggestOptions.execute_params(results_response, save_query)

            if cmd == UserSuggestOptions.CONT:
                wait_on_user = False
            elif cmd == UserSuggestOptions.QUIT:
                time_to_quit = True
                break

        if time_to_quit:
            break

