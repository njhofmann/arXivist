from __future__ import annotations
from typing import List, Tuple, Callable
import src.api.retrieve_paper as rp
import src.modes.search_options as so
import src.utility.search_result as sr
import src.utility.save_query as sq
import src.util as u

"""Mode for searching for and saving papers from arXiv."""


def create_result_display_func(responses: List[Tuple[int, sr.SearchResult]]) -> Callable:
    def print_results():
        for result_id, response in responses:
            print(result_id, response.title)
    return print_results


def search_mode():
    print('search mode entered')
    params = u.get_formatted_user_input('enter search params')

    print('fetching results...')
    search_query = rp.SearchQuery.from_args(params)
    print('results fetched')

    save_query = sq.SaveQuery()
    for responses in search_query.retrieve_search_results():
        time_to_quit = False
        responses_print_func = create_result_display_func(responses)
        for result_id, response in responses:
            save_query.add_valid_id(result_id, response)

        responses_print_func()

        while True:
            so.UserSearchOptions.display_available_options()
            results_response = u.get_formatted_user_input()
            cmd = so.UserSearchOptions.execute_params(results_response, save_query)

            if cmd == so.UserSearchOptions.CONT:
                break
            elif cmd == so.UserSearchOptions.QUIT:
                time_to_quit = True
                break
            elif cmd == so.UserSearchOptions.DISP:
                responses_print_func()

        if time_to_quit:
            break
