from __future__ import annotations

from typing import List

import src.api.retrieve_paper as rp
import src.database.retrieve as dbr
import src.utility.cmd_enum as ce
import src.utility.save_query as sq
import src.modes.search_options as so
import src.util as u

"""Module for suggesting new papers to a user based on previously saved papers."""


def suggest_mode():
    suggested_ids = dbr.get_suggested_papers()
    results = rp.SearchQuery(id_args=suggested_ids).retrieve_search_results()

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
            cmd = so.UserSearchOptions.execute_params(results_response, save_query)

            if cmd == so.UserSearchOptions.CONT:
                wait_on_user = False
            elif cmd == so.UserSearchOptions.QUIT:
                time_to_quit = True
                break

        if time_to_quit:
            break
