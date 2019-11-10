from typing import List, Any, Tuple, Map
import retrieve_paper as rp
import enum as e
import sys


BAD_CHARS = (' ')


class UserSearchResponses(e.Enum):
    MORE = 'more'
    CONT = 'cont'
    VIEW = 'view'
    ADD = 'add'
    QUIT = 'quit'

    def __eq__(self, other: Any) -> bool:
        if isinstance(UserSearchResponses, other):
            return self == other
        elif isinstance(str, other):
            return other == self.value
        return False


def is_list_of_n_ints(to_parse: List[str], n: int = -1) -> List[int]:
    if not to_parse:
        return []
    elif n > -1 and len(to_parse) != n:  # -1 means variable length
        raise ValueError(f'given list {to_parse} must have only {n} entries')

    for idx, entry in enumerate(to_parse):
        to_parse[idx] = int(entry)
    return to_parse


def validate_user_result_response(response: List[str]) -> Tuple[UserSearchResponses, List[int]]:
    if not response or response[0] not in UserSearchResponses:
        raise ValueError(f"response must be one of {','.join([_ for _ in UserSearchResponses])}")

    cmd, params = response[0], response[1:]
    if cmd == UserSearchResponses.MORE:
        return UserSearchResponses.MORE, is_list_of_n_ints(params, 1)
    elif cmd == UserSearchResponses.ADD:
        return UserSearchResponses.ADD, is_list_of_n_ints(params)
    elif cmd == UserSearchResponses.CONT:
        return UserSearchResponses.CONT, is_list_of_n_ints(params, 0)
    elif cmd == UserSearchResponses.QUIT:
        return UserSearchResponses.QUIT, is_list_of_n_ints(params, 0)
    else:
        return UserSearchResponses.VIEW, is_list_of_n_ints(params, 0)


class SaveQuery:

    def __init__(self):
        self.selected_ids: List[id] = []
        self.valid_ids_to_info: Map[int, rp.SearchQuery] = {}

    def add_valid_id(self, result_id: int, result: rp.SearchQuery) -> None:
        if result_id in self.valid_ids_to_info:
            raise ValueError(f'id {result_id} already added to list of valid ids')
        self.valid_ids_to_info[result_id] = result

    def add_id(self, param: int) -> None:
        if param not in self.valid_ids_to_info:
            raise ValueError(f'{param} not in list of valid ids')
        self.selected_ids.append(param)

    def __str__(self):
        if self.selected_ids:
            return f"save query: {', '.join(self.selected_ids)}"
        return 'nothing in save query'

    def submit(self) -> None:
        pass


def delete_last_line():
    sys.stdout.write('\x1b[1A')  # move cursor up one line
    sys.stdout.write('\x1b[2K')  # delete last line


def format_params(params: List[str]) -> List[str]:
    for idx, param in enumerate(params):
        for char in BAD_CHARS:
            param = param.replace(char, '')
        params[idx] = param
    return list(filter(lambda x: bool(x), params))


def main():
    while True:
        try:
            params = input('enter search params\n')
            params = format_params(params.split(' '))
            search_query = rp.SearchQuery.from_params(params)

            save_query = SaveQuery()
            for responses in search_query.retrieve_search_results():
                for response in responses:
                    id = response[0]
                    title = response[1]
                    save_query.add_valid_id(id, response[1])
                    print(id, title)
                results_response = input("""
                options: 
                  - 'more id' to view more info\n
                  - 'cont' to view more results\n
                  - 'add ids' to add results to save query\n
                  - 'view' to view current save query
                  - 'quit' to terminate responses and submit save query\n
                """)

                cmd, params = validate_user_result_response(results_response)

                if cmd == UserSearchResponses.MORE:
                    print()
                elif cmd == UserSearchResponses.ADD:
                    for param in params:
                        save_query.add_id(param)
                elif cmd == UserSearchResponses.CONT:
                    continue
                elif cmd == UserSearchResponses.QUIT:
                    save_query.submit()
                    break
                elif cmd == UserSearchResponses.VIEW:
                    print(save_query)


                for _ in responses:  # TODO fix clearing
                    delete_last_line()

        except Exception as e:
            print(str(e))


if __name__ == '__main__':
    main()