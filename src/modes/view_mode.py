from __future__ import annotations

from typing import List

import src.database.insert as dbi
import src.database.remove as rm
import src.database.retrieve as dbr
import src.db_util as dbu
import src.pdf_utils as pu
import src.util as u
import src.utility.cmd_enum as ce
import src.utility.save_query as sq

"""Mode for viewing, removing, or editing previously saved entries."""


def quit_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    u.is_list_of_n_ints(args, 0)


def cont_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    u.is_list_of_n_ints(args, 0)


def more_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    selected_id = u.is_list_of_n_ints(args, 1)[0]
    if not save_query.is_valid_id(selected_id):
        raise ValueError(f'selected id {selected_id} is not a valid id')
    print(save_query.get_result(selected_id))


def open_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    selected_id = u.is_list_of_n_ints(args, 1)[0]
    if not save_query.is_valid_id(selected_id):
        raise ValueError(f'selected id {selected_id} is not a valid id')
    pu.open_pdf(save_query.get_result(selected_id).pdf_path)


def help_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    u.is_list_of_n_ints(args, 0)
    UserViewModes.display_help_options()


def del_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    paper_idx = u.is_list_of_n_ints(args, 1)[0]
    if not save_query.is_valid_id(paper_idx):
        raise ValueError(f'invalid id {paper_idx}')
    paper_id = int(save_query.get_result(paper_idx).id)
    rm.remove_paper(paper_id)
    print(f'removed paper {paper_id}')


def key_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    # TODO finish me
    if len(args) < 2:
        raise ValueError('need at least a paper id and one keyword')
    paper_id = int(args[0])
    keywords = args[1:]
    dbu.generic_db_query(dbi.insert_keywords, paper_id, keywords)


def rmv_cmd_func(args: List[str], save_query: sq.SaveQuery) -> None:
    if len(args) != 2:
        raise ValueError('need a paper id and a keyword')
    paper_id = int(args[0])
    rm.remove_keyword(save_query.valid_ids_to_info[paper_id].id, args[1])


class UserViewModes(ce.CmdEnum):
    QUIT = ce.Command('quit', quit_cmd_func, 'quit the mode')
    CONT = ce.Command('cont', cont_cmd_func, 'continue viewing more search results')
    MORE = ce.Command('more', more_cmd_func, 'view summary info about a selected pdf')
    #OPEN = ce.Command('open', open_cmd_func, 'open a file for viewing')
    HELP = ce.Command('help', help_cmd_func, 'view what each option does')
    DEL = ce.Command('del', del_cmd_func, 'removes paper and associated data')
    KEY = ce.Command('key', key_cmd_func, 'for adding a keyword to a retrieved paper')
    RMV = ce.Command('rmv', rmv_cmd_func, 'for removing a keyword from a retrieved paper')

    @classmethod
    def execute_params(cls, params: List[str], save_query: sq.SaveQuery = None) -> UserViewModes:
        return UserViewModes(super().execute_params_with_checks(params, save_query))


def view_mode():
    print('view mode entered')
    db_query = dbr.DatabaseQuery.from_args()
    results = db_query.get_results()
    save_query = sq.SaveQuery()

    time_to_quit = False
    for response in results:
        response_print_func = u.create_result_display_func(response)
        response_print_func()

        while True:
            results_response = u.get_formatted_user_input('waiting...')
            cmd = UserViewModes.execute_params(results_response, save_query)

            if cmd == UserViewModes.CONT:
                break
            elif cmd == UserViewModes.QUIT:
                time_to_quit = True
                break

        if time_to_quit:
            break
