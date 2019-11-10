import utility as u
import db_retrieve as dbr
import search_mode as sm
from typing import List, Tuple, Union
import pdf_utils as pu


class UserViewModes(u.EqualEnum):
    QUIT = 'quit'
    CONT = 'cont'
    MORE = 'more'
    OPEN = 'open'


def validate_user_result_response(response: List[str], save_query: sm.SaveQuery) -> UserViewModes
    if not response:
        raise ValueError(f"not provided a response, must be one of {UserViewModes.values_as_str()}")

    cmd, params = response[0], response[1:]
    if not UserViewModes.is_valid_response(cmd):
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
            pu.open_paper(save_query.get_result(selected_id))
        return UserViewModes.OPEN


def view_mode():
    while True:
        search_params = input('enter search params').split(' ')
        results = dbr.DatabaseQuery.from_params(search_params)

        save_query = sm.SaveQuery()
        for idx, result in results:
            save_query.add_valid_id(idx, result)
            print(idx, result.title)

