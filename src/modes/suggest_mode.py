from __future__ import annotations

from typing import List

import src.api.retrieve_paper as rp
import src.database.retrieve as dbr
import src.utility.cmd_enum as ce
import src.utility.save_query as sq
import src.util as u

"""Module for suggesting new papers to a user based on previously saved papers."""


def add_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    ids = u.is_list_of_n_ints(args)
    for result_id in ids:
        save_query.select_id(result_id)


def cont_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    u.is_list_of_n_ints(args, 0)


def quit_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    u.is_list_of_n_ints(args, 0)
    save_query.submit()


def view_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    u.is_list_of_n_ints(args, 0)
    print(save_query)


def more_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    selected_id = u.is_list_of_n_ints(args, 1)[0]
    if not save_query.is_valid_id(selected_id):
        raise ValueError(f'selected id {selected_id} is not a valid id')
    print(save_query.get_result(selected_id))


def help_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    u.is_list_of_n_ints(args, 0)
    UserSuggestOptions.display_help_options()


class UserSuggestOptions(ce.CmdEnum):
    ADD = ce.Command('add', add_cmd_func, 'to add papers to the query of papers to retrieve')
    CONT = ce.Command('cont', cont_cmd_func, 'to view more results')
    QUIT = ce.Command('quit', quit_cmd_func, 'to quit viewing this mode')
    MORE = ce.Command('more', more_cmd_func, 'to view more information about a previously displayed paper')
    VIEW = ce.Command('view', view_cmd_func, 'to view what papers have been added to the queue of papers to save')
    HELP = ce.Command('help', help_cmd_func, 'to view what each option does')

    @classmethod
    def execute_params(cls, params: List[str], save_query: sq.SaveQuery = None) -> UserSuggestOptions:
        return UserSuggestOptions(super().execute_params_with_checks(params, save_query))


def suggest_mode():
    suggested_ids = dbr.get_suggested_papers()
    results = rp.SearchQuery(id_params=suggested_ids).retrieve_search_results()

    print('entered suggest mode')
    save_query = sq.SaveQuery()
    for response in results:
        time_to_quit = False
        for idx, result in response:
            save_query.add_valid_id(idx, result)
            print(idx, result.title)

        wait_on_user = True
        while wait_on_user:
            results_response = u.get_formatted_user_input('waiting')
            cmd = UserSuggestOptions.execute_params(results_response, save_query)

            if cmd == UserSuggestOptions.CONT:
                wait_on_user = False
            elif cmd == UserSuggestOptions.QUIT:
                time_to_quit = True
                break

        if time_to_quit:
            break
