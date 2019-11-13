import utility
import utility as u
import db_retrieve as dbr
import search_mode as sm
from typing import List, Tuple, Union
import pdf_utils as pu


class UserViewModes(u.CommandEnum):
    QUIT = 'quit'
    CONT = 'cont'
    MORE = 'more'
    OPEN = 'open'


def validate_user_result_response(response: List[str], save_query: utility.SaveQuery) -> UserViewModes:
    if not response:
        raise ValueError(f"not provided a response, must be one of {UserViewModes.values_as_str()}")

    cmd, params = response[0], response[1:]
    if not UserViewModes.is_valid(cmd):
        raise ValueError(f"invalid response {cmd}, must be one of {UserViewModes.values_as_str()}")

    if cmd == UserViewModes.MORE:
        selected_id = u.is_list_of_n_ints(params, 1)[0]
        if not save_query.is_valid_id(selected_id):
            raise ValueError(f'selected id {selected_id} is not a valid id')
        else:
            print(save_query.get_result(selected_id))
        return UserViewModes.MORE
    elif cmd == UserViewModes.CONT:
        return UserViewModes.CONT
    elif cmd == UserViewModes.QUIT:
        u.is_list_of_n_ints(params, 0)
        return UserViewModes.QUIT
    else:
        selected_id = u.is_list_of_n_ints(params, 1)[0]
        if not save_query.is_valid_id(selected_id):
            raise ValueError(f'selected id {selected_id} is not a valid id')
        else:
            pu.open_pdf(save_query.get_result(selected_id).pdf_path)
        return UserViewModes.OPEN


def view_mode():
    search_params = [param for param in input('enter search params\n').split(' ') if param]
    db_query = dbr.DatabaseQuery.from_params(search_params)

    results = db_query.get_results()
    save_query = utility.SaveQuery()

    for response in results:
        time_to_quit = False
        for idx, result in response:
            save_query.add_valid_id(idx, result)
            print(idx, result.title)

            print("\noptions:\n"
                  "- 'more id' to view more info\n"
                  "- 'cont' to view more results\n"
                  "- 'open id' to open current selected paper\n"
                  "- 'quit' to terminate viewing\n")

            wait_on_user = True
            while wait_on_user:
                results_response = input('waiting...\n')
                results_response = [result for result in results_response.split(' ') if result]
                cmd = validate_user_result_response(results_response, save_query)

                if cmd == UserViewModes.CONT:
                    wait_on_user = False
                elif cmd == UserViewModes.QUIT:
                    time_to_quit = True
                    break

        if time_to_quit:
            break
