from __future__ import annotations
import src.utility.search_result as sr
from database import retrieve as dbr
from typing import List
import src.utility.save_query as sq
import src.database.remove as rm
import src.pdf_utils as pu
import src.utility.command_enum as ce

"""Mode for viewing, removing, or editing previously saved entries."""


class UserViewModes(ce.CommandEnum):
    QUIT = 'quit'  # quit the mode
    CONT = 'cont'  # continue viewing more search results
    MORE = 'more'  # view summary info about a selected pdf
    OPEN = 'open'  # open a file for viewing
    HELP = 'help'  # view what each option does
    DEL = 'del'  # removes paper and associated data
    KEY = 'key'  # for adding a keyword to a retrieved paper

    @classmethod
    def execute_params(cls, params: List[str], save_query: sq.SaveQuery = None) -> UserViewModes:
        super().execute_params(params, save_query)
        cmd, params = params[0], params[1:]

        if cmd == UserViewModes.MORE:
            selected_id = ce.is_list_of_n_ints(params, 1)[0]
            if not save_query.is_valid_id(selected_id):
                raise ValueError(f'selected id {selected_id} is not a valid id')
            print(save_query.get_result(selected_id))
            return UserViewModes.MORE

        elif cmd == UserViewModes.CONT:
            ce.is_list_of_n_ints(params, 0)
            return UserViewModes.CONT

        elif cmd == UserViewModes.QUIT:
            ce.is_list_of_n_ints(params, 0)
            return UserViewModes.QUIT

        elif cmd == UserViewModes.DEL:
            paper_idx = ce.is_list_of_n_ints(params, 1)[0]
            if not save_query.is_valid_id(paper_idx):
                raise ValueError(f'invalid id {paper_idx}')
            paper_id = save_query.get_result(paper_idx).id
            rm.remove_paper(paper_id)
            print(f'removed paper {paper_id}')
            return UserViewModes.DEL

        elif cmd == UserViewModes.KEY:
            # TODO finish me
            return UserViewModes.KEY

        elif cmd == UserViewModes.HELP:
            ce.is_list_of_n_ints(params, 0)
            print("\noptions:\n"
                  "- 'more id' to view more info\n"
                  "- 'cont' to view more results\n"
                  "- 'open id' to open current selected paper\n"
                  "- 'del id' to remove a retrieved paper"
                  "- 'key id word' to add a keyword to a paper"
                  "- 'quit' to terminate viewing\n")
            return UserViewModes.HELP

        else:
            selected_id = ce.is_list_of_n_ints(params, 1)[0]
            if not save_query.is_valid_id(selected_id):
                raise ValueError(f'selected id {selected_id} is not a valid id')
            else:
                pu.open_pdf(save_query.get_result(selected_id).pdf_path)
            return UserViewModes.OPEN


def view_mode():
    search_params = sr.split_and_format_string(input('enter search params\n'))
    db_query = dbr.DatabaseQuery.from_params(search_params)
    results = db_query.get_results()
    save_query = sq.SaveQuery()

    time_to_quit = False
    for response in results:
        for idx, result in response:
            save_query.add_valid_id(idx, result)
            print(idx, result.title)

        print('view mode entered\n')

        while True:
            results_response = sr.split_and_format_string(input('waiting...\n'))
            cmd = UserViewModes.execute_params(results_response, save_query)

            if cmd == UserViewModes.CONT:
                break
            elif cmd == UserViewModes.QUIT:
                time_to_quit = True
                break

        if time_to_quit:
            break