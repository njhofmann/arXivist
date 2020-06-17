from __future__ import annotations

from typing import List

import src.api.retrieve_paper as rp
import src.util as u
import src.utility.cmd_enum as ce
import src.utility.save_query as sq
import util

"""Mode for searching for and saving papers from arXiv."""


def more_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    selected_id = util.is_list_of_n_ints(args, 1)[0]
    if not save_query.is_valid_id(selected_id):
        raise ValueError(f'selected id {selected_id} is not a valid id')
    print(save_query.get_result(selected_id))


def add_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    for param in args:
        save_query.select_id(int(param))
    util.is_list_of_n_ints(args)


def cont_cmd_func(params: List[str], save_query: sq.SaveQuery) -> None:
    util.is_list_of_n_ints(params, 0)


def quit_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    save_query.submit()
    util.is_list_of_n_ints(args, 0)


def view_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    util.is_list_of_n_ints(args, 0)
    print(save_query)


def help_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    util.is_list_of_n_ints(args, 0)
    UserSearchResponses.display_help_options()


class UserSearchResponses(ce.CmdEnum):
    MORE = ce.Command('more', more_cmd_func, 'view summary info selected paper')
    CONT = ce.Command('cont', cont_cmd_func, 'continue seeing new search results')
    VIEW = ce.Command('view', view_cmd_func, 'what files have been added to the query of files to saved')
    ADD = ce.Command('add', add_cmd_func, 'add paper to query to be saved')
    QUIT = ce.Command('quit', quit_cmd_func, 'quit this mode')
    HELP = ce.Command('help', help_cmd_func, 'view what each option does')

    @classmethod
    def execute_params(cls, args: List[str], save_query: sq.SaveQuery = None) -> UserSearchResponses:
        return UserSearchResponses(super().execute_params_with_checks(args, save_query))


def search_mode():
    print('search mode entered')
    params = u.get_formatted_user_input('enter search params')

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
            UserSearchResponses.display_available_options()
            results_response = u.get_formatted_user_input()
            cmd = UserSearchResponses.execute_params(results_response, save_query)

            if cmd == UserSearchResponses.CONT:
                break
            elif cmd == UserSearchResponses.QUIT:
                time_to_quit = True
                break

        if time_to_quit:
            break
