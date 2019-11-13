from typing import List, Tuple, Union
import utility as u
import retrieve_paper as rp
from db_insert import SaveQuery


class UserSearchResponses(u.CommandEnum):
    MORE = 'more'
    CONT = 'cont'
    VIEW = 'view'
    ADD = 'add'
    QUIT = 'quit'


def validate_user_result_response(response: List[str], save_query: SaveQuery) -> Tuple[UserSearchResponses,
                                                                                       Union[int, List[int]]]:
    if not response:
        raise ValueError(f"not provided a response, must be one of {UserSearchResponses.values_as_str()}")

    cmd, params = response[0], response[1:]
    if not UserSearchResponses.is_valid(cmd):
        raise ValueError(f"invalid response {cmd}, must be one of {UserSearchResponses.values_as_str()}")

    if cmd == UserSearchResponses.MORE:
        selected_id = u.is_list_of_n_ints(params, 1)[0]
        if not save_query.is_valid_id(selected_id):
            raise ValueError(f'selected id {selected_id} is not a valid id')
        return UserSearchResponses.MORE, selected_id
    elif cmd == UserSearchResponses.ADD:
        return UserSearchResponses.ADD, u.is_list_of_n_ints(params)
    elif cmd == UserSearchResponses.CONT:
        return UserSearchResponses.CONT, u.is_list_of_n_ints(params, 0)
    elif cmd == UserSearchResponses.QUIT:
        return UserSearchResponses.QUIT, u.is_list_of_n_ints(params, 0)
    else:
        return UserSearchResponses.VIEW, u.is_list_of_n_ints(params, 0)


def format_params(params: List[str]) -> List[str]:
    for idx, param in enumerate(params):
        for char in (' '):
            param = param.replace(char, '')
        params[idx] = param
    return list(filter(lambda x: bool(x), params))


def search_mode():
    params = input('enter search params\n')
    params = format_params(params.split(' '))
    search_query = rp.SearchQuery.from_params(params)

    save_query = SaveQuery()
    for responses in search_query.retrieve_search_results():
        time_to_quit = False
        for result_id, response in responses:
            title = response.title
            save_query.add_valid_id(result_id, response)
            print(result_id, title)

        print("\noptions:\n"
              "- 'more id' to view more info\n"
              "- 'cont' to view more results\n"
              "- 'add ids' to add results to save query\n"
              "- 'view' to view current save query\n"
              "- 'quit' to terminate responses and submit save query")

        wait_on_user = True
        while wait_on_user:
            results_response = input('waiting...\n')
            results_response = [result for result in results_response.split(' ') if result]
            cmd, params = validate_user_result_response(results_response, save_query)

            if cmd == UserSearchResponses.MORE:
                print(save_query.get_result(params))
            elif cmd == UserSearchResponses.ADD:
                for param in params:
                    save_query.select_id(param)
            elif cmd == UserSearchResponses.CONT:
                wait_on_user = False
            elif cmd == UserSearchResponses.QUIT:
                save_query.submit()
                time_to_quit = True
                break
            elif cmd == UserSearchResponses.VIEW:
                print(save_query)

        if time_to_quit:
            break