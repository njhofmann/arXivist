from __future__ import annotations
from typing import List
import psycopg2 as psy

import src.database.retrieve as dbr
import src.api.retrieve_paper as rp
import src.utility.save_query as sq
import src.utility.cmd_enum as ce
import src.db_init as dbi

"""Module for suggesting new papers to a user based on previously saved papers."""


class UserSuggestOptions(ce.CmdEnum):
    ADD = 'add'  # to add papers to the query of papers to retrieve
    CONT = 'cont'  # to view more results
    QUIT = 'quit'  # to quit viewing this mode
    MORE = 'more'  # to view more information about a previously displayed paper
    VIEW = 'view'  # to view what papers have been added to the queue of papers to save
    HELP = 'help'  # to view what each option does

    @classmethod
    def execute_params(cls, params: List[str], save_query: sq.SaveQuery = None) -> UserSuggestOptions:
        super().execute_params(params, save_query)
        cmd, params = params[0], params[1:]

        if cmd == UserSuggestOptions.MORE:
            selected_id = ce.is_list_of_n_ints(params, 1)[0]
            if not save_query.is_valid_id(selected_id):
                raise ValueError(f'selected id {selected_id} is not a valid id')
            print(save_query.get_result(selected_id))
            return UserSuggestOptions.MORE

        elif cmd == UserSuggestOptions.ADD:
            ids = ce.is_list_of_n_ints(params)
            for result_id in ids:
                save_query.select_id(result_id)
            return UserSuggestOptions.ADD

        elif cmd == UserSuggestOptions.CONT:
            ce.is_list_of_n_ints(params, 0)
            return UserSuggestOptions.CONT

        elif cmd == UserSuggestOptions.QUIT:
            ce.is_list_of_n_ints(params, 0)
            save_query.submit()
            return UserSuggestOptions.QUIT

        elif cmd == UserSuggestOptions.HELP:
            ce.is_list_of_n_ints(params, 0)
            print("\noptions:\n"
                  "- 'more id' to view more info about a paper\n"
                  "- 'cont' to view more results\n"
                  "- 'add ids' to add results\n"
                  "- 'view' to see what papers will be saved\n"
                  "- 'quit' to terminate viewing suggestions, save any papers in the save queue")
            return UserSuggestOptions.HELP

        else:  # must be view
            ce.is_list_of_n_ints(params, 0)
            print(save_query)
            return UserSuggestOptions.VIEW


def suggest_mode():
    with psy.connect(dbname=dbi.get_db_info().db_name) as conn:
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

        print('entered suggest mode\n')

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
