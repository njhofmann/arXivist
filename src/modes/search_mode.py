from __future__ import annotations
from typing import List
import src.utility.search_result as sr
import src.api.retrieve_paper as rp
import src.utility.save_query as sq
import src.utility.cmd_enum as ce
import src.util as u

"""Mode for searching for and saving papers from arXiv."""


class UserSearchResponses(ce.CmdEnum):
    MORE = 'more'  # view summary info selected paper
    CONT = 'cont'  # continue seeing new search results
    VIEW = 'view'  # what files have been added to the query of files to saved
    ADD = 'add'  # add paper to query to be saved
    QUIT = 'quit'  # quit this mode
    HELP = 'help'  # view what each option does

    @classmethod
    def execute_params(cls, params: List[str], save_query: sq.SaveQuery = None) -> UserSearchResponses:
        super().execute_params(params, save_query)

        cmd, params = params[0], params[1:]

        if cmd == UserSearchResponses.MORE:
            selected_id = ce.is_list_of_n_ints(params, 1)[0]
            if not save_query.is_valid_id(selected_id):
                raise ValueError(f'selected id {selected_id} is not a valid id')
            print(save_query.get_result(selected_id))
            return UserSearchResponses.MORE

        elif cmd == UserSearchResponses.ADD:
            for param in params:
                save_query.select_id(int(param))
            ce.is_list_of_n_ints(params)
            return UserSearchResponses.ADD

        elif cmd == UserSearchResponses.CONT:
            ce.is_list_of_n_ints(params, 0)
            return UserSearchResponses.CONT

        elif cmd == UserSearchResponses.QUIT:
            save_query.submit()
            ce.is_list_of_n_ints(params, 0)
            return UserSearchResponses.QUIT

        elif cmd == UserSearchResponses.HELP:
            ce.is_list_of_n_ints(params, 0)
            print("\noptions:\n"
                  "- 'more id' to view more info about a resulting paper\n"
                  "- 'cont' to view more search results\n"
                  "- 'add ids' to add results to save query\n"
                  "- 'view' to view current save query\n"
                  "- 'quit' to terminate responses and submit save query")
            return UserSearchResponses.HELP

        else:
            ce.is_list_of_n_ints(params, 0)
            print(save_query)
            return UserSearchResponses.VIEW


def format_params(params: List[str]) -> List[str]:
    for idx, param in enumerate(params):
        for char in ' ':
            param = param.replace(char, '')
        params[idx] = param
    return list(filter(lambda x: bool(x), params))


def search_mode():
    print('search mode entered')
    params = format_params(u.get_user_input('enter search params').split(' '))

    print('fetching results...')
    search_query = rp.SearchQuery.from_params(params)
    print('results fetched')

    save_query = sq.SaveQuery()
    for responses in search_query.retrieve_search_results():
        time_to_quit = False
        for result_id, response in responses:
            title = response.title
            save_query.add_valid_id(result_id, response)
            print(result_id, title)

        while True:
            user_response = u.get_user_input('')
            results_response = sr.split_and_format_string(user_response)
            cmd = UserSearchResponses.execute_params(results_response, save_query)

            if cmd == UserSearchResponses.CONT:
                break
            elif cmd == UserSearchResponses.QUIT:
                time_to_quit = True
                break

        if time_to_quit:
            break
